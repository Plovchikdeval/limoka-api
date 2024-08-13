from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.db.functions import Developer, Module
from app.protect import verify_token_main

from app.utils.parser import get_git_modules, get_module, get_module_info

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{developer_telegram_id}")
async def get_developer(developer_telegram_id: int):
    """
    Get developer by id.
    :param developer_telegram_id: Developer id.
    :return: Developer dict.
    """
    developer = await Developer.get_dict(developer_telegram_id)
    return developer


@router.post("/", dependencies=[Depends(verify_token_main)])
async def create_developer(developer_telegram_id: int, username: str, git: str):
    """
    Create developer.
    :param developer_telegram_id: Developer id.
    :param username: Username.
    :param git: Git.
    :return: Developer dict.
    """
    developer = await Developer.create_developer(developer_telegram_id, username, git)
    modules = get_git_modules(git)

    for module in modules:
        code = get_module(module, git)
        try:
            info = get_module_info(code)
        except Exception as e:
            print(e)
            continue

        await Module.create_module(
            module,
            info["description"],
            developer_telegram_id,
            hash(code),
            git + module + ".py",
            info["pic"],
            info["commands"],
            code
        )
    return developer
