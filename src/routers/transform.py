from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
from PIL import Image
from io import BytesIO


router = APIRouter()

# Mirror (Left-Right)
@router.get("/transform/mirror/{ImageId}")
async def mirror_image(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

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
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename=mirror.png"
        }
    )    

# Flip (Up-Down)
@router.get("/transform/flip/{ImageId}")
async def flip_image(ImageId: str):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

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
            "Content-Disposition": f"inline; filename=flipped.png"
        }
    )    


# Rotate image
@router.get("/transform/rotate/{ImageId}")
async def rotate_image(ImageId: str, degrees: int):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

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
            "Content-Disposition": f"inline; filename=rotated_{degrees}.png"
        }
    )    


# Resize image
@router.get("/transform/resize/{ImageId}")
async def resize_image(ImageId: str, width: int, height: int):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

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
            "Content-Disposition": f"inline; filename=resized_{width}x{height}.png"
        }
    )    


# Crop image
@router.get("/transform/crop/{ImageId}")
async def crop_image(ImageId: str, left: int, top: int, right: int, bottom: int):
    contents = await db["images"].find_one({"_id": ObjectId(ImageId)})

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = BytesIO(contents["data"])

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
            "Content-Disposition": f"inline; filename=cropped_{left}x{top}x{right}x{bottom}.png"
        }
    )    
