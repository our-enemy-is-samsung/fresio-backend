from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.refrigerator.schema.ingredient_detail import IngredientItemSchema


class AddIngredientDTO(BaseSchema):
    name: str = Field(..., description="재료 이름", examples=["토마토"])
    quantity: str = Field(..., description="수량", examples=["1"])
    icon: str = Field(..., description="아이콘", examples=["🍅"])
    items: list[IngredientItemSchema] = Field(..., description="재료 목록")
