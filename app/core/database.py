from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]