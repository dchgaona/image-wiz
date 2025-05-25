from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
import io

router = APIRouter()


@router.get("/images/{ImageId}")
async def get_image(ImageId: str):
    objInstance = ObjectId(ImageId)
    contents = await db["images"].find_one({"_id": objInstance})
    

    if not contents:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes = io.BytesIO(contents["data"])

    return StreamingResponse(
        image_bytes,
        media_type=contents["content-type"],
        headers={
            "Content-Disposition": f"inline; filename={contents["filename"]}"
        }
    )


@router.post("/images/")
async def post_image(image: UploadFile = File(...)):
    contents = await image.read()

    result = await db["images"].insert_one(
        {
            "filename": image.filename,
            "content-type": image.content_type,
            "data": Binary(contents)
        }
    )

    return {
        "Message": "Image uploaded",
        "Image Id": str(result.inserted_id)
        }


