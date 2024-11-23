from uuid import UUID

from pydantic import Field
from datetime import datetime

from app.application.pydantic_model import BaseSchema
from app.application.typevar import UNICODE_EMOJI, IMAGE_URL


class ExpiringFoodItemSchema(BaseSchema):
    id: UUID = Field(..., description="식재료 ID")
    icon: UNICODE_EMOJI | IMAGE_URL = Field(..., description="아이콘")
    name: str = Field(..., description="식재료 이름")
    expired_at: datetime = Field(..., description="유통기한")
    quantity: int = Field(..., description="수량")
