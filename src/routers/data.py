from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
from PIL import Image
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
async def change_format(ImageId: str, new_format: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    
    if new_format.casefold() not in formats:
        raise HTTPException(status_code=400, detail=f"Not valid format. List of valid formats: {formats.keys()}")
    

    image_bytes = BytesIO(contents["data"])

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
async def compress_image(ImageId: str, quality_level: int):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    if quality_level > 100 or quality_level < 1:
        raise HTTPException(status_code=400, detail="quality_level can't be greater than 100 or lower than 1")
    

    image_bytes = BytesIO(contents["data"])

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
            "Content-Disposition": f"inline; filename=compressed.webp"
        }
    )    



    

    
    

    

async def get_position(pos, w, h):
    match pos:
        case "TOP_LEFT":
            return (0,0)
        case "BOTTOM_LEFT":
            return (0, h)
        case "TOP_RIGHT":
            return (w, 0)
        case "BOTTOM_RIGHT":
            return (w, h)
        case "CENTER":
            return (w / 2, h / 2)
