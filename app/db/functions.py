from typing import Union

from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    """
    User model, contains all methods for working with users.
    """
    @classmethod
    async def get_dict(cls, tg_id: int) -> Union[dict, None]:
        """
        Get user by id.
        :param user_id: User id.
        :return: User dict.
        """
        try:
            return await cls.get(telegram_id=tg_id)
        except DoesNotExist:
            return None
        
    @classmethod
    async def create_user(cls, telegram_id: int) -> dict:
        """
        Create user.
        :param telegram_id: Telegram id.
        :return: User dict.
        """
        user = await cls.create(telegram_id=telegram_id)
        return user
    
    @classmethod
    async def get_count(cls) -> int:
        """
        Get count of users.
        :return: Count of users.
        """
        return await cls.all().count()


class Developer(models.Developer):
    """
    Developer model, contains all methods for working with developers.
    """
    @classmethod
    async def get_dict(cls, tg_id: int) -> Union[dict, None]:
        """
        Get developer by id.
        :param tg_id: Developer id.
        :return: Developer dict.
        """
        try:
            return await cls.get(telegram_id=tg_id)
        except DoesNotExist:
            return None
        
    @classmethod
    async def get_dict_by_username(cls, username: str) -> Union[dict, None]:
        """
        Get developer by username.
        :param username: Username.
        :return: Developer dict.
        """
        try:
            return await cls.get(username=username)
        except DoesNotExist:
            return None
        
    @classmethod
    async def create_developer(cls, telegram_id: int, username: str, git: str) -> dict:
        """
        Create developer.
        :param telegram_id: Telegram id.
        :param username: Username.
        :param git: Git.
        :return: Developer dict.
        """
        developer = await cls.create(telegram_id=telegram_id, username=username, git=git, is_verified=False)
        return developer


class Module(models.Module):
    """
    Module model, contains all methods for working with modules.
    """
    @classmethod
    async def get_dict(cls, module_id: int) -> Union[dict, None]:
        """
        Get module by id.
        :param module_id: Module id.
        :return: Module dict.
        """
        try:
            return await cls.get(id=module_id)
        except DoesNotExist:
            return None

    @classmethod
    async def create_module(cls, name: str, description: str, developer: int, hash: str, git: str, image: str, commands: list, code: str) -> dict:
        """
        Create module.
        :param name: Name.
        :param description: Description.
        :param developer: Developer id.
        :param hash: Hash.
        :param git: Git.
        :param image: Image.
        :param commands: Commands.
        :param code: Code.
        :return: Module dict.
        """
        module = await cls.create(name=name, description=description, developer=developer, hash=hash, git=git, image=image, commands=commands, downloads=[], looks=[], code=code)
        return module

    @classmethod
    async def add_download(cls, user_id: int, module_id: int):
        """
        Add download.
        :param user_id: User id.
        :param module_id: Module id.
        """
        module = await cls.get_dict(module_id)

        if module is None:
            return

        if user_id not in module.downloads:
            module.downloads.append(user_id)
            await module.save()

    @classmethod
    async def add_look(cls, user_id: int, module_id: int):
        """
        Add look.
        :param user_id: User id.
        :param module_id: Module id.
        """
        module = await cls.get_dict(module_id)

        if module is None:
            return

        if user_id not in module.looks:
            module.looks.append(user_id)
            await module.save()

    @classmethod
    async def get_top(cls):
        """
        Get top modules.
        :return: Top modules.
        """
        return await cls.all().order_by("-downloads").limit(10)

    @classmethod
    async def get_all(cls):
        """
        Get all modules.
        :return: All modules.
        """
        # all modules without code
        return await cls.all().values("id", "name", "description", "developer", "hash", "git", "image", "commands", "downloads", "looks")

    @classmethod
    async def get_raw_module(cls, developer: int, module_name: str):
        """
        Get raw module.
        :param developer_id: Developer id.
        :param module_name: Module name.
        :return: Raw module.
        """
        module = await cls.get(developer=developer, name=module_name)

        if module is None:
            return

        return module.code
