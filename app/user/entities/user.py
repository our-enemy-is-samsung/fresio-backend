from tortoise import Model, fields


class User(Model):
    id: str = fields.UUIDField(pk=True)
    name: str = fields.CharField(max_length=100)
    email: str = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "users"
