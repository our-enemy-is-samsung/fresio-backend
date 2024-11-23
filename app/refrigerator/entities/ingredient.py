from tortoise import fields
from tortoise.models import Model


class Ingredient(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    expired_at = fields.DatetimeField()
    quantity = fields.IntField()
    icon = fields.TextField()
    items = fields.JSONField(default=[])

    class Meta:
        table = "ingredients"
