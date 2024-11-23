from tortoise import Model, fields

from app.hardware.entities import Hardware


class User(Model):
    id: str = fields.UUIDField(pk=True)
    name: str = fields.CharField(max_length=100)
    device_id: str = fields.TextField()
    meal_type: str = fields.CharField(max_length=100)

    camera_hardware = fields.ForeignKeyField(
        "models.Hardware", related_name="camera_user", null=True
    )
    display_hardware = fields.ForeignKeyField(
        "models.Hardware", related_name="display_user", null=True
    )

    class Meta:
        table = "users"
