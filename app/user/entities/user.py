from tortoise import Model, fields


class User(Model):
    id: str = fields.UUIDField(pk=True)
    name: str = fields.CharField(max_length=100)
    device_id: str = fields.TextField()
    meal_type: str = fields.CharField(max_length=100)
    food_check: str = fields.CharField(max_length=100)

    camera_hardware = fields.ForeignKeyField(
        "models.Hardware", related_name="camera_user", null=True
    )
    display_hardware = fields.ForeignKeyField(
        "models.Hardware", related_name="display_user", null=True
    )
    refrigerator = fields.ManyToManyField(
        "models.Ingredient",
        related_name="users",
        through="user_refrigerator",
        null=True,
    )

    class Meta:
        table = "users"
