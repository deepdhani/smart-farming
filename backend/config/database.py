# config/database.py — MongoDB connection via Motor (async)

import motor.motor_asyncio
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017/smart_farming"
    jwt_secret: str = "change_this_secret"
    jwt_expire_hours: int = 72
    openweather_api_key: str = ""
    environment: str = "development"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

# MongoDB client (shared across app)
client: motor.motor_asyncio.AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
    db = client.smart_farming
    print("✅ Connected to MongoDB")


async def disconnect_db():
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB")


def get_db():
    return db
