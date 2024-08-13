from fastapi import APIRouter, Depends, Response
from app.protect import verify_token_main

from app.db.functions import Module, Developer

router = APIRouter()


@router.get("/all")
async def get_modules():
    modules = await Module.get_all()
    return modules


@router.get("/{module_id}")
async def get_module(module_id: int):
    module = await Module.get_dict(module_id=module_id)
    return module


@router.get("/{developer_username}/{module_name}.py")
async def get_raw_module(developer_username: str, module_name: str):
    developer = await Developer.get_dict_by_username(developer_username)
    if developer is None:
        return {"error": "Developer not found."}
    module = await Module.get_raw_module(developer.telegram_id, module_name)
    return Response(content=module, media_type="text/plain")


@router.put("/look/{module_id}/{user_id}", dependencies=[Depends(verify_token_main)])
async def look_module(module_id: int, user_id: int):
    module = await Module.add_look(module_id=module_id, user_id=user_id)
    return module


@router.put("/download/{module_id}/{user_id}", dependencies=[Depends(verify_token_main)])
async def download_module(module_id: int, user_id: int):
    module = await Module.add_download(module_id=module_id, user_id=user_id)
    return module
