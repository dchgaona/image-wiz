from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from mongo.database_handler import db
from bson.objectid import ObjectId
from auth.dependencies import get_current_user
from models import UserInDB
from bson.binary import Binary
from io import BytesIO

router = APIRouter()

formats = {
    "jpeg": "JPEG",
    "jpg":  "JPEG",
    "png": "PNG",
    "bmp": "BMP",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
    "webp": "WEBP"
}

# Change image format
@router.get("/data/format/{ImageId}")
async def change_format(ImageId: str, new_format: str, current_user: UserInDB = Depends(get_current_user)):

    """
    Change the format of an image to a specified format.
    - **ImageId**: The ID of the image to be converted.
    - **new_format**: The desired format for the image (e.g., jpeg, png, webp).
    - **Valid formats**: jpeg, jpg, png, bmp, gif, tif, tiff, webp.
    """
    
    users = await db["users"].find_one({"_id": current_user._id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")
    
    if new_format.casefold() not in formats:
        raise HTTPException(status_code=400, detail=f"Not valid format. List of valid formats: {formats.keys()}")
    

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        output_buffer = BytesIO()
        original_image.save(output_buffer, format=formats[new_format])
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type=f"image/{formats[new_format].casefold()}",
        headers={
            "Content-Disposition": f"inline; filename=new_format.{new_format}"
        }
    )    


# Compress image
@router.get("/data/compress/{ImageId}")
async def compress_image(ImageId: str, quality_level: int, current_user: UserInDB = Depends(get_current_user)):
    
    """
    Compress an image to a specified quality level.
    - **ImageId**: The ID of the image to be compressed.
    - **quality_level**: The quality level for compression (1-100).
    """

    users = await db["users"].find_one({"_id": current_user._id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")


    if quality_level > 100 or quality_level < 1:
        raise HTTPException(status_code=400, detail="quality_level can't be greater than 100 or lower than 1")
    

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        w, h = original_image.size

        original_image = original_image.resize((w, h), Image.LANCZOS)

        output_buffer = BytesIO()
        original_image.save(output_buffer, format="WEBP", optimize=True, quality=quality_level)
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type=f"image/webp",
        headers={
            "Content-Disposition": f"inline; filename=compressed_{ImageId}.webp"
        }
    )    


# Add watermark to image
@router.post("/data/watermark/{ImageId}")
async def add_watermark(ImageId: str, watermark: UploadFile = File(None), text: str = None, position: str = "BOTTOM_RIGHT", current_user: UserInDB = Depends(get_current_user)):    
    """
    Add a watermark to an image by either uploading a watermark image or providing text.
    - **ImageId**: The ID of the image to which the watermark will be added.
    - **watermark**: An optional watermark image file.
    - **text**: Optional text to be used as a watermark.
    - **position**: The position of the watermark on the image. Default is "BOTTOM_RIGHT".
    """

    
    users = await db["users"].find_one({"_id": current_user._id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")


    if not watermark and not text:
        raise HTTPException(status_code=400, detail="You must provide either a watermark image or text")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)
        w, h = original_image.size

        if watermark:
            watermark_bytes = await watermark.read()
            watermark_image = Image.open(BytesIO(watermark_bytes)).convert("RGBA")
            
            max_wm_w = w // 4
            max_wm_h = h // 4
            wm_w, wm_h = watermark_image.size
            
            if wm_w > max_wm_w or wm_h > max_wm_h:
                ratio = min(max_wm_w / wm_w, max_wm_h / wm_h)
                new_size = (int(wm_w * ratio), int(wm_h * ratio))
                watermark_image = watermark_image.resize(new_size, Image.LANCZOS)
                wm_w, wm_h = watermark_image.size

            pos_x, pos_y = await get_position(position, w, h, wm_w, wm_h)
            original_image.paste(watermark_image, (pos_x, pos_y), watermark_image)

        if text:
            draw = ImageDraw.Draw(original_image)
            
            
            font_size = min(w, h) // 30
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            
            if text_w > w // 3:
                ratio = (w // 3) / text_w
                font_size = int(font_size * ratio)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
            
            pos_x, pos_y = await get_position(position, w, h, text_w, text_h)
            
            outline_color = "black"
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                draw.text((pos_x + dx, pos_y + dy), text, font=font, fill=outline_color)
            draw.text((pos_x, pos_y), text, font=font, fill="white")

        output_buffer = BytesIO()
        original_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=watermarked_{ImageId}.png"
        }
    )
    

    
    


async def get_position(position: str, width: int, height: int, content_width: int, content_height: int) -> tuple:
 
    padding = 10  # pixels de margem
    
    if position == "TOP_LEFT":
        return (padding, padding)
    elif position == "BOTTOM_LEFT":
        return (padding, height - content_height - padding)
    elif position == "TOP_RIGHT":
        return (width - content_width - padding, padding)
    elif position == "BOTTOM_RIGHT":
        return (width - content_width - padding, height - content_height - padding)
    elif position in ["CENTER", "WHOLE"]:
        return ((width - content_width) // 2, (height - content_height) // 2)
    else:
        raise HTTPException(status_code=400, detail="Invalid position specified")