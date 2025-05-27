from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
from PIL import Image
from auth.dependencies import get_current_user
from models import UserInDB
from io import BytesIO


router = APIRouter()

# Mirror (Left-Right)
@router.get("/transform/mirror/{ImageId}")
async def mirror_image(ImageId: str, current_user: UserInDB = Depends(get_current_user)):
    
    """
    Mirror an image horizontally.
    - **ImageId**: The ID of the image to be mirrored.
    """

    user = await db["users"].find_one({"_id": current_user.id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = original_image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type=f"image/png",
        headers={
            "Content-Disposition": f"inline; filename=mirror_{ImageId}.png"
        }
    )    

# Flip (Up-Down)
@router.get("/transform/flip/{ImageId}")
async def flip_image(ImageId: str, current_user: UserInDB = Depends(get_current_user)):

    """
    Flip an image vertically.
    - **ImageId**: The ID of the image to be flipped.
    """

    user = await db["users"].find_one({"_id": current_user.id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = original_image.transpose(method=Image.Transpose.TOP_BOTTOM)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=flipped_{ImageId}.png"
        }
    )    


# Rotate image
@router.get("/transform/rotate/{ImageId}")
async def rotate_image(ImageId: str, degrees: int, current_user: UserInDB = Depends(get_current_user)):
    
    """
    Rotate an image by a specified number of degrees.
    - **ImageId**: The ID of the image to be rotated.
    - **degrees**: The number of degrees to rotate the image.
    """

    user = await db["users"].find_one({"_id": current_user.id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = original_image.rotate(degrees)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=rotated_{degrees}_{ImageId}.png"
        }
    )    


# Resize image
@router.get("/transform/resize/{ImageId}")
async def resize_image(ImageId: str, width: int, height: int, current_user: UserInDB = Depends(get_current_user)):
    
    """
    Resize an image to specified dimensions.
    - **ImageId**: The ID of the image to be resized.
    - **width**: The new width of the image.
    - **height**: The new height of the image.
    """

    user = await db["users"].find_one({"_id": current_user.id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = original_image.resize((width, height))

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=resized_{width}x{height}_{ImageId}.png"
        }
    )    


# Crop image
@router.get("/transform/crop/{ImageId}")
async def crop_image(ImageId: str, left: int, top: int, right: int, bottom: int, current_user: UserInDB = Depends(get_current_user)):
    
    """
    Crop an image to specified dimensions.
    - **ImageId**: The ID of the image to be cropped.
    - **left**: The left coordinate of the crop rectangle.
    - **top**: The top coordinate of the crop rectangle.
    - **right**: The right coordinate of the crop rectangle.
    - **bottom**: The bottom coordinate of the crop rectangle.
    """
    
    user = await db["users"].find_one({"_id": current_user.id})

    if not user or "images" not in user or ImageId not in  user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = user["images"][ImageId]
    image_bytes = BytesIO(image_data["content"])

    try:
        original_image = Image.open(image_bytes)
        width, height = original_image.size

        modified_image = original_image.crop((left / width, top / height, right, bottom)).resize((width, height))
        

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=cropped_{left}x{top}x{right}x{bottom}_{ImageId}.png"
        }
    )    
