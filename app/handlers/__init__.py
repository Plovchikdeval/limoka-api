from fastapi import APIRouter
from app.handlers.user.api import router as user_router
from app.handlers.module.api import router as module_router
from app.handlers.developer.api import router as developer_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(module_router, prefix="/module", tags=["module"])
router.include_router(developer_router, prefix="/developer", tags=["developer"])


@router.get("/")
async def api_root():
    return {"ping": "pong"}
