from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.color import TimerColor
from app.timer.schema.cooktimer_detail import CookTimerStepSchema


class CookTimerCreateSchema(BaseSchema):
    name: str = Field(..., description="타이머 이름")
    color: TimerColor = Field(..., description="타이머 색상")
    emoji: str = Field(..., description="타이머 이모지")
    description: str = Field(..., description="타이머 설명")
    steps: list[CookTimerStepSchema] = Field(..., description="타이머 단계")
