from typing import TYPE_CHECKING, Optional
from tortoise.models import Model
from tortoise import fields

if TYPE_CHECKING:
    from app.user.entities import User


class Hardware(Model):
    id: str = fields.UUIDField(pk=True)
    device_id: str = fields.CharField(max_length=100, unique=True)
    device_type: str = fields.CharField(max_length=100)
    token: str = fields.CharField(max_length=100)
    user_id: str = fields.TextField()
