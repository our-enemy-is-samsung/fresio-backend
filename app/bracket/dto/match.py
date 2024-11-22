from typing import Literal
from pydantic import Field
from app.application.pydantic_model import BaseSchema


class MatchTypeDTO(BaseSchema):
    match_type: Literal["single", "double"] = Field(
        ..., description="매칭타입 선택 (single: 단식, double: 복식)"
    )
