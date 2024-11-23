from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.color import TimerColor


class CookTimerStepSchema(BaseSchema):
    time: int = Field(0, description="분")
    recipe: str = Field(..., description="레시피")


class CookTimerDetailSchema(BaseSchema):
    id: UUID = Field(..., description="타이머 ID")
    name: str = Field(..., description="타이머 이름")
    color: TimerColor = Field(..., description="타이머 색상")
    emoji: str = Field(..., description="타이머 이모지")
    steps: list[CookTimerStepSchema] = Field(..., description="타이머 단계")
    created_at: datetime = Field(..., description="생성일")
    updated_at: datetime = Field(..., description="수정일")
