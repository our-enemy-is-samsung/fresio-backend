from typing import Literal

from pydantic import Field

from app.application.pydantic_model import BaseSchema


class GroupSchema(BaseSchema):
    group_id: str = Field(..., description="그룹 ID")
    name: str = Field(..., description="그룹 이름")


class GroupListSchema(BaseSchema):
    groups: list[GroupSchema] = Field(..., description="그룹 목록")


class StudentSchema(BaseSchema):
    student_id: str = Field(..., description="학생 ID")
    name: str = Field(..., description="학생 이름")
    gender: Literal["male", "female"] = Field(
        ..., description="성별"
    )  # male=남, female=여 로 변환
    level: Literal["상", "중", "하"] | None = Field(None, description="등급")


class StudentListSchema(BaseSchema):
    students: list[StudentSchema] = Field(..., description="학생 목록")
