from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import RegisterReq
from auth import auth, jwt

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(register_req: RegisterReq):
    auth.register_user(register_req.username, register_req.password)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}