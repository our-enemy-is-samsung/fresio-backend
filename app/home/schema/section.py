from uuid import UUID

from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.cook_difficulty import CookDifficulty


class PersonalizedRecommendationRecipeSchema(BaseSchema):
    recipe_id: UUID = Field(..., description="레시피 ID")
    ingredients: list[str] = Field(..., description="재료 목록")
    name: str = Field(..., description="요리 이름")
    difficulty: CookDifficulty = Field(..., description="난이도")
    estimated_time: int = Field(..., description="예상 소요 시간 (분)")


class PersonalizedRecommendationSectionSchema(BaseSchema):
    section_name: str = Field(
        ..., description="섹션 이름", examples=["서늘한 저녁 이 음식은 어떤가요?"]
    )
    recipes: list[PersonalizedRecommendationRecipeSchema] = Field(
        ..., description="레시피 목록"
    )


class PersonalizedRecommendationSchema(BaseSchema):
    sections: list[PersonalizedRecommendationSectionSchema] = Field(
        ..., description="추천 섹션 목록"
    )
