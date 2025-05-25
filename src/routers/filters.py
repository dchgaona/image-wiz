from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO
import numpy as np


router = APIRouter()

# Grayscale filter
@router.get("/filter/grayscale/{ImageId}")
async def grayscale(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = ImageOps.grayscale(original_image)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename=grayscaled.jpeg"
        }
    )    


# Negative filter
@router.get("/filter/negative/{ImageId}")
async def negative(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = ImageOps.invert(original_image)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename=negative.jpeg"
        }
    )    


# Posterize filter
@router.get("/filter/posterize/{ImageId}")
async def posterize(ImageId: str, bits: int):
    if bits > 8 or bits < 1:
        raise HTTPException(500, detail="Posterize bits can't be greater than 8 or less than 1")

    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = ImageOps.posterize(original_image, bits)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename=posterized.jpeg"
        }
    )    


# Sepia filter
@router.get("/filter/sepia/{ImageId}")
async def sepia(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

    try:
        image = Image.open(image_bytes).convert("RGB")

        image = np.asarray(image).astype(np.float32)  / 255.0
        

        R, G, B = image[...,0], image[...,1], image[...,2]
        image_out = np.dstack((0.393 * R + 0.769 * G + 0.189 * B, \
                               0.349 * R + 0.686 * G + 0.168 * B, \
                               0.272 * R + 0.534 * G + 0.131 * B))
        
        image_out = np.clip(image_out, 0, 1)

        image_result = (255*image_out).astype(np.uint8)
        image_result = Image.fromarray(image_result)

        output_buffer = BytesIO()
        image_result.save(output_buffer, format="JPEG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename=sepia.jpeg"
        }
    )    


# Sharpen image
@router.get("/filter/sharpen/{ImageId}")
async def sharpen(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

    try:
        original_image = Image.open(image_bytes)

        modified_image = original_image.filter(ImageFilter.SHARPEN)

        output_buffer = BytesIO()
        modified_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)

    except Exception as e:
        raise HTTPException(400, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(
        output_buffer,
        media_type="image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename=sharpened.jpeg"
        }
    )    
