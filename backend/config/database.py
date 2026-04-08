# config/database.py — MongoDB connection via Motor (async)

import motor.motor_asyncio
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ✅ Your actual values (hardcoded for now)
    mongo_uri: str = "mongodb+srv://db_user:Deepak12@deepak.2pheyms.mongodb.net/smart_farming?appName=deepak"
    jwt_secret: str = "smartfarming_secret_key_2024"
    jwt_expire_hours: int = 72
    openweather_api_key: str = "53d9124f6798290b4eeaafa1d232c392"
    environment: str = "production"

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
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
        db = client.smart_farming

        # ✅ Test connection
        await client.admin.command("ping")

        print("✅ Connected to MongoDB")

    except Exception as e:
        print("❌ MongoDB Connection Error:", e)


async def disconnect_db():
    global client
    if client:
        client.close()
        print("🔌 Disconnected from MongoDB")


def get_db():
    return db
