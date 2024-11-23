from enum import Enum
from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.meal import MealType


class AgeEnum(str, Enum):
    age_10 = "10대"
    age_20 = "20대"
    age_30 = "30대"
    age_40 = "40대"
    age_50 = "50대"
    age_60 = "60대"


class FoodCheckEnum(str, Enum):
    too_much = "과다"
    just_right = "적정"
    too_little = "소식"


class FoodCheckFormDTO(BaseSchema):
    food_check_pasta: FoodCheckEnum = Field(..., title="파스타")
    food_check_pizza: FoodCheckEnum = Field(..., title="밥")
    food_check_cutlet: FoodCheckEnum = Field(..., title="치킨")
    food_check_ramen: FoodCheckEnum = Field(..., title="샐러드")
    food_check_bibimbap: FoodCheckEnum = Field(..., title="초밥")


class DeviceLoginDTO(BaseSchema):
    device_id: str = Field(..., title="디바이스 ID")


class DeviceRegisterDTO(BaseSchema):
    device_id: str = Field(..., title="디바이스 ID")
    age: AgeEnum = Field(..., title="나이")
    name: str = Field(..., title="이름")
    meal_type: MealType = Field(..., title="식사 타입")
    food_check: FoodCheckFormDTO = Field(..., title="음식 섭취량")
