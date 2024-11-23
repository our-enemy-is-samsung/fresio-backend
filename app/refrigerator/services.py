from app.refrigerator.entities import Ingredient
from app.user.entities import User


class RefrigeratorService:

    @staticmethod
    async def get_ingredients(user: User) -> list[Ingredient]:
        await user.fetch_related("refrigerator")
