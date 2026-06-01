from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def _get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGO_URI,
            maxPoolSize=10,
            serverSelectionTimeoutMS=5000,
        )
    return _client


def get_db():
    return _get_client()[settings.DB_NAME]


def col(name: str):
    """Return a MongoDB collection by name."""
    return get_db()[name]
