from fastapi import APIRouter, Depends
from app.protect import verify_token_main

from app.db.functions import User

router = APIRouter()


@router.get("/count")
async def get_count():
    count = await User.get_count()
    return {"count": count}


@router.get("/{user_id}")
async def get_user(tg_id: int):
    user = await User.get_dict(tg_id=tg_id)
    return user or {"error": "User not found."}


@router.post("/", dependencies=[Depends(verify_token_main)])
async def create_user(telegram_id: int):
    if await User.get_dict(tg_id=telegram_id):
        return {"error": "User already exists."}

    user = await User.create_user(telegram_id=telegram_id)
    return user
