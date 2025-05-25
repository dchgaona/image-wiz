from fastapi import FastAPI
from routers import images, transform

app = FastAPI()

app.include_router(images.router, prefix="/api")
app.include_router(transform.router,  prefix="/api")

@app.get("/")
async def root():
    return 
    {
        "status": "ok",
        "version": "1.0.0"
    }