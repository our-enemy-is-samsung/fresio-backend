from pydantic import Field
from uuid import UUID

from app.application.pydantic_model import BaseSchema
from app.enums.cook_difficulty import CookDifficulty


class RecommendRecipeSchema(BaseSchema):
    id: UUID = Field(..., description="레시피 ID")
    name: str = Field(..., description="레시피 이름")
    image_url: str = Field(..., description="레시피 이미지 URL")
    cook_time: int = Field(..., description="요리 시간 (분)")
    difficulty: CookDifficulty = Field(..., description="난이도")
