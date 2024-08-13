from fastapi import HTTPException, Header

from app.config import parse_config


async def verify_token_main(token: str = Header("token")):
    config = parse_config()
    if not token == config.token.get_config()["main"]:
        raise HTTPException(status_code=403, detail="Unauthorized token.")
