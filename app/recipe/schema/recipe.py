from uuid import UUID

from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.application.typevar import IMAGE_URL


class RecipeIngredientSchema(BaseSchema):
    name: str = Field(..., description="재료 이름")
    amount: str = Field(..., description="재료 양")


class RecipeTimerStepSchema(BaseSchema):
    description: str = Field(..., description="타이머 설명")
    time: int = Field(..., description="타이머 시간 (분)")


class RecipeTimerSchema(BaseSchema):
    background_color: str = Field(..., description="타이머 배경 색상")
    emoji: str = Field(..., description="타이머 이모지")
    steps: list[RecipeTimerStepSchema] = Field(..., description="타이머 단계")


class RecipeDetailSchema(BaseSchema):
    id: UUID = Field(..., description="레시피 ID")
    name: str = Field(..., description="레시피 이름")
    thumbnail_image: IMAGE_URL = Field(..., description="레시피 썸네일")
    estimated_time: int = Field(..., description="예상 소요 시간 (분)")
    servings: int = Field(..., description="인분")
    ingredients: list[RecipeIngredientSchema] = Field(..., description="재료 목록")
    steps: list[str] = Field(..., description="요리 순서")
    timer: RecipeTimerSchema = Field(..., description="타이머 정보")
