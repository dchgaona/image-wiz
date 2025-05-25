from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = AsyncMongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB_NAME")]