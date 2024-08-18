from fastapi import APIRouter, Depends, Response
from app.protect import verify_token_main
from app.utils.parser import get_git_modules, get_module, get_module_info

from app.db.functions import Module, Developer, Updates
from app.utils.diff import get_diff, get_html_diff

router = APIRouter()


@router.get("/all")
async def get_modules():
    modules = await Module.get_all()
    return modules


@router.get("/{module_id}")
async def get_module_dict(module_id: int):
    module = await Module.get_dict(module_id=module_id)
    return {
        "id": module.id,
        "name": module.name,
        "description": module.description,
        "developer": module.developer,
        "hash": module.hash,
        "image": module.image,
        "banner": module.banner,
        "commands": module.commands,
        "downloads": len(module.downloads),
        "looks": len(module.looks)
    }


# @router.get("/{developer_username}/{module_name}.py")
# async def get_raw_module(developer_username: str, module_name: str):
#     developer = await Developer.get_dict_by_username(developer_username)
#     if developer is None:
#         return {"error": "Developer not found."}
#     module = await Module.get_raw_module(developer_username, module_name)
#     return Response(content=module, media_type="text/plain")


@router.get("/download/{module_id}")
async def get_raw_module(module_id: int):
    module = await Module.get_dict(module_id=module_id)
    if module is None:
        return {"error": "Module not found."}
    module = module.code
    return Response(content=module, media_type="text/plain")


@router.put("/look/{module_id}/{user_id}", dependencies=[Depends(verify_token_main)])
async def look_module(module_id: int, user_id: int):
    module = await Module.add_look(module_id=module_id, user_id=user_id)
    return module


@router.put("/download/{module_id}/{user_id}", dependencies=[Depends(verify_token_main)])
async def download_module(module_id: int, user_id: int):
    module = await Module.add_download(module_id=module_id, user_id=user_id)
    return module


@router.get("/check_updates/", dependencies=[Depends(verify_token_main)])
async def check_updates():
    all_developers = await Developer.all()

    for developer in all_developers:
        # modules_in_db = await Module.get_modules_by_developer(developer.telegram_id)
        modules_in_db = [module.name for module in await Module.get_modules_by_developer(developer.telegram_id)]
        unapproved_updates = [update.name for update in await Updates.get_dict_unapproved()]
        modules_in_git = get_git_modules(developer.git)

        for module in modules_in_git:
            code = get_module(module, developer.git)
            try:
                info = get_module_info(code)
            except Exception as e:
                print(e)
                continue

            if not info:
                continue

            if module not in modules_in_db and module not in unapproved_updates:
                await Updates.create_update(
                    name=module,
                    description=info["description"],
                    developer=developer.username,
                    git=developer.git,
                    image=info["meta"]["pic"],
                    banner=info["meta"]["banner"],
                    commands=info["commands"],
                    new_code=code
                )
                continue

            if module in modules_in_db:
                module_db = await Module.get_dict_by_name(module)
                code = get_module(module, developer.git)
                if code != module_db.code:
                    await Updates.create_update(
                        name=module,
                        description=info["description"],
                        developer=developer.username,
                        git=developer.git,
                        image=info["meta"]["pic"],
                        banner=info["meta"]["banner"],
                        commands=info["commands"],
                        new_code=code,
                    )

    return {"status": "ok"}


@router.get("/approve_update/{update_id}", dependencies=[Depends(verify_token_main)])
async def approve_update(update_id: int):
    update = await Updates.get_dict(update_id)
    if update is None:
        return {"error": "Update not found."}
    await Updates.approve_update(update_id)
    link = ""
    if update.git.endswith("/"):
        link = update.git + update.name + ".py"
    else:
        link = update.git + "/" + update.name + ".py"
    await Module.create_module(
        update.name,
        update.description,
        update.developer,
        hash(update.new_code),
        link,
        update.image,
        update.banner,
        update.commands,
        update.new_code
    )
    return {"status": "ok"}


@router.get("/get_unapproved_updates/", dependencies=[Depends(verify_token_main)])
async def get_unapproved_updates():
    updates = await Updates.get_dict_unapproved()
    return updates


@router.get("/get_diff/{update_id}/{type}")
async def get_diff_update(update_id: int, type: str):
    update = await Updates.get_dict(update_id)
    if update is None:
        return {"error": "Update not found."}

    module = await Module.get_dict_by_name(update.name)
    code = ""
    if module is not None:
        code = module.code

    if type == "html":
        return Response(
            content=get_html_diff(code, update.new_code), media_type="text/html"
        )
    return Response(
        content=get_diff(code, update.new_code), media_type="text/plain"
    )
