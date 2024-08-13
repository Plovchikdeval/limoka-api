from fastapi import FastAPI
from app.version import branch, get_info
from app.handlers import router as handlers_router


def dispatcher(context):
    app = FastAPI()
    app.include_router(router=handlers_router, prefix="/api")

    @app.get("/")
    async def root():
        git_info = get_info(branch)
        return {"name": "limoka", "start_time": context["start_time"], **git_info}

    return app
