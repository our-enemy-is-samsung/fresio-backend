from typing import Literal

from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.meal import MealType


class DeviceLoginDTO(BaseSchema):
    device_id: str = Field(..., title="디바이스 ID")


class DeviceRegisterDTO(BaseSchema):
    device_id: str = Field(..., title="디바이스 ID")
    name: str = Field(..., title="이름")
    meal_type: MealType = Field(..., title="식사 타입")
