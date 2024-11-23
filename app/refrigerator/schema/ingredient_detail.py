from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.application.pydantic_model import BaseSchema


class IngredientItemSchema(BaseSchema):
    id: UUID = Field(..., description="재료 ID")
    name: str = Field(..., description="재료 이름", examples=["토마토"])
    created_at: datetime = Field(
        ..., description="생성일", examples=["2021-10-01T00:00:00"]
    )
    expired_at: datetime = Field(
        ..., description="수정일", examples=["2021-10-01T00:00:00"]
    )
    quantity: int = Field(..., description="수량", examples=[1])
    thumbnail_image: str = Field(
        ..., description="재료 썸네일", examples=["https://example.com/image"]
    )


class IngredientDetailSchema(BaseSchema):
    id: UUID = Field(..., description="상품 ID")
    name: str = Field(..., description="상품 이름", examples=["토마토"])
    created_at: datetime = Field(
        ..., description="생성일", examples=["2021-10-01T00:00:00"]
    )
    expired_at: datetime = Field(
        ..., description="수정일", examples=["2021-10-01T00:00:00"]
    )
    quantity: int = Field(..., description="수량", examples=[1])
    thumbnail_image: str = Field(
        ..., description="상품 썸네일", examples=["https://example.com/image"]
    )
    ingredient_list: list[IngredientItemSchema] = Field(..., description="재료 목록")
