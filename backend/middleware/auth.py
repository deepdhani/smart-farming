from fastapi import APIRouter, HTTPException
from config.database import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register")
async def register(user: dict):
    db = get_db()

    try:
        print("🔥 Incoming:", user)

        # ✅ Validate required fields
        if not user.get("phone") or not user.get("password"):
            raise HTTPException(status_code=400, detail="Phone and password required")

        # ✅ Check existing user
        existing = await db.users.find_one({"phone": user["phone"]})
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        # ✅ Hash password
        user["password"] = hash_password(user["password"])

        # ✅ Insert safely
        result = await db.users.insert_one(user)

        print("✅ Inserted:", result.inserted_id)

        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ FULL ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
