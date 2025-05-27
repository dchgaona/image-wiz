from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from mongo.database_handler import db
from bson.objectid import ObjectId
from bson.binary import Binary
from auth.dependencies import get_current_user
from models import UserInDB
import io

router = APIRouter()

@router.post("/images/upload")
async def upload_image(
    image: UploadFile = File(...),
    description: str = Form(None),
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        image_content = await image.read()
        image_data = {
            "id": str(ObjectId()),
            "filename": image.filename,
            "content": Binary(image_content),
            "description": description,
            "content_type": image.content_type
        }
        
        
        result = await db["users"].update_one(
            {"_id": current_user._id},
            {
                "$set": {
                    f"images.{image_data['id']}": image_data
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to upload image")
            
        return {"message": "Image uploaded successfully", "image_id": image_data["id"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/{image_id}")
async def get_image(
    image_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    user = await db["users"].find_one({"_id": current_user._id})
    
    if not user or "images" not in user or image_id not in user["images"]:
        raise HTTPException(status_code=404, detail="Image not found")
        
    image_data = user["images"][image_id]
    return StreamingResponse(
        io.BytesIO(image_data["content"]),
        media_type=image_data["content_type"]
    )

@router.get("/images")
async def get_all_images(current_user: UserInDB = Depends(get_current_user)):
    user = await db["users"].find_one({"_id": current_user._id})
    
    if not user or "images" not in user:
        return {"images": {}}
        
    
    images_list = {}
    for image_id, image_data in user["images"].items():
        images_list[image_id] = {
            "id": image_id,
            "filename": image_data["filename"],
            "description": image_data["description"],
            "content_type": image_data["content_type"]
        }
    
    return {"images": images_list}

@router.delete("/images/{image_id}")
async def delete_image(
    image_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    result = await db["users"].update_one(
        {"_id": current_user._id},
        {"$unset": {f"images.{image_id}": ""}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Image not found")
        
    return {"message": "Image deleted successfully"}

@router.delete("/images")
async def delete_all_images(current_user: UserInDB = Depends(get_current_user)):
    result = await db["users"].update_one(
        {"_id": current_user._id},
        {"$set": {"images": {}}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to delete images")
        
    return {"message": "All images deleted successfully"}

