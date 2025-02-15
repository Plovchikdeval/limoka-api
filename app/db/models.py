from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True, unique=True)
    telegram_id = fields.BigIntField()

class Developer(Model):
    id = fields.BigIntField(pk=True, unique=True)
    telegram_id = fields.BigIntField()
    username = fields.CharField(max_length=255)

    git = fields.CharField(max_length=255)
    is_verified = fields.BooleanField()

class Module(Model):
    id = fields.BigIntField(pk=True, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    developer = fields.CharField(max_length=255)
    hash = fields.CharField(max_length=255)
    git = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255, null=True)
    banner = fields.CharField(max_length=525, null=True)
    commands = fields.JSONField(null=True)
    # [ { "command": "description" } ]
    code = fields.TextField(null=True)

class Updates(Model):
    id = fields.BigIntField(pk=True, unique=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    developer = fields.CharField(max_length=255)
    git = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255, null=True)
    banner = fields.CharField(max_length=525, null=True)
    commands = fields.JSONField(null=True)
    new_code = fields.TextField()
    approved = fields.BooleanField()
