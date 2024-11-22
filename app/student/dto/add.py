from typing import Literal
from pydantic import Field

from app.application.pydantic_model import BaseSchema


class AddStudentDTO(BaseSchema):
    name: str = Field(..., description="학생 이름")
    gender: Literal["male", "female"] = Field(..., description="성별")
    level: Literal["상", "중", "하"] = Field(..., description="등급")
