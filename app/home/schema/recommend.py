from uuid import UUID
from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.cook_difficulty import CookDifficulty


class CookingRecommendSchema(BaseSchema):
    recipie_id: UUID = Field(
        ..., description="레시피 ID", examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    recommend_title: str = Field(
        ..., description="추천 텍스트", examples=["서늘한 저녁 이 음식은 어떤가요?"]
    )
    title: str = Field(
        ..., description="요리 이름", examples=["바나나 버터구이 프렌치 토스트"]
    )
    image_url: str = Field(
        ..., description="요리 이미지 URL", examples=["https://image_url.com"]
    )
    difficulty: CookDifficulty = Field(..., description="난이도", examples=["easy"])
    estimated_time: int = Field(..., description="예상 소요 시간 (분)")


class ServiceRecommendSchema(BaseSchema):
    recommend_id: UUID = Field(
        ..., description="추천 ID", examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    ui_small_top_text: str = Field(
        ..., description="추천 상단 작은 텍스트", examples=["가장 많이 찾는"]
    )
    ui_main_text: str = Field(
        ..., description="추천 중앙 텍스트", examples=["라면 타이머 실행하기"]
    )
    internal_deep_link: str = Field(..., description="딥링크", examples=["timer/index"])


class RecommendationSchema(BaseSchema):
    recipe: CookingRecommendSchema = Field(
        ..., description="레시피 추천", examples=[{}]
    )
    service: ServiceRecommendSchema = Field(
        ..., description="서비스 추천", examples=[{}]
    )
