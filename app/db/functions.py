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

    @classmethod
    async def get_all(cls) -> list:
        """
        Get all users.
        :return: All users.
        """
        users = await cls.all().values("telegram_id")
        return [user["telegram_id"] for user in users]


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
    
    @classmethod
    async def get_all(cls) -> list:
        """
        Get all developers.
        :return: All developers.
        """
        developers = await cls.all()
        return developers


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
    async def get_dict_by_name(cls, module_name: str) -> Union[dict, None]:
        """
        Get module by name.
        :param module_name: Module name.
        :return: Module dict.
        """
        try:
            return await cls.get(name=module_name)
        except DoesNotExist:
            return None

    @classmethod
    async def create_module(cls, name: str, description: str, developer: int, hash: str, git: str, image: str, banner: str, commands: list, code: str) -> dict:
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
        if await cls.get_dict_by_name(name) is not None:
            # update module
            module = await cls.get_dict_by_name(name)
            module.description = description
            module.developer = developer
            module.hash = hash
            module.git = git
            module.image = image
            module.banner = banner
            module.commands = commands
            module.code = code
            await module.save()
            return module
        module = await cls.create(name=name, description=description, developer=developer, hash=hash, git=git, image=image, banner=banner, commands=commands, code=code)
        return module

    @classmethod
    async def get_all(cls):
        """
        Get all modules.
        :return: All modules.
        """
        # all modules without code
        return await cls.all().values("id", "name", "description", "developer", "hash", "git", "image", "banner", "commands")

    @classmethod
    async def get_modules_by_developer(cls, developer: int):
        """
        Get modules by developer.
        :param developer: Developer id.
        :return: Modules by developer.
        """
        return await cls.filter(developer=developer)

    @classmethod
    async def get_raw_module(cls, developer: int, module_name: str):
        """
        Get raw module.
        :param developer_id: Developer id.
        :param module_name: Module name.
        :return: Raw module.
        """
        try:
            return (await cls.get(developer=developer, name=module_name)).code
        except DoesNotExist:
            return ""


class Updates(models.Updates):
    """
    Updates model, contains all methods for working with updates.
    """
    @classmethod
    async def get_dict_unapproved(cls) -> Union[dict, None]:
        """
        Get unapproved update.
        :return: Update dict.
        """
        try:
            return await cls.all().filter(approved=False)
        except DoesNotExist:
            return None

    @classmethod
    async def get_dict_all(cls) -> Union[dict, None]:
        """
        Get all updates.
        :return: Update dict.
        """
        try:
            return await cls.all()
        except DoesNotExist:
            return None

    @classmethod
    async def get_dict(cls, update_id: int) -> Union[dict, None]:
        """
        Get update by id.
        :param update_id: Update id.
        :return: Update dict.
        """
        try:
            return await cls.get(id=update_id)
        except DoesNotExist:
            return None
        
    @classmethod
    async def get_dict_by_name(cls, name: str) -> Union[dict, None]:
        """
        Get update by name.
        :param name: Name.
        :return: Update dict.
        """
        try:
            return await cls.get(name=name)
        except DoesNotExist:
            return None

    @classmethod
    async def create_update(cls, name: str, description: str, developer: str, git: str, image: str, banner: str, commands: list, new_code: str) -> dict:
        """
        Create update.
        :param name: Name.
        :param description: Description.
        :param developer: Developer.
        :param git: Git.
        :param image: Image.
        :param banner: Banner.
        :param commands: Commands.
        :param new_code: New code.
        :return: Update dict.
        """
        if await cls.get_dict_by_name(name) is not None:
            # remove old update
            update = await cls.get_dict_by_name(name)
            await update.delete()
        update = await cls.create(name=name, description=description, developer=developer, git=git, image=image, banner=banner, commands=commands, new_code=new_code, approved=False)
        return update    

    @classmethod
    async def approve_update(cls, update_id: int):
        """
        Approve update.
        :param update_id: Update id.
        """
        update = await cls.get_dict(update_id)

        if update is None:
            return

        update.approved = True
        await update.save()
