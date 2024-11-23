from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.enums.color import TimerColor


class CookTimerUpdateSchema(BaseSchema):
    name: str | None = Field(None, description="타이머 이름")
    color: TimerColor | None = Field(None, description="타이머 색상")
    emoji: str | None = Field(None, description="타이머 이모지")


class CookTimerStepUpdateSchema(BaseSchema):
    time: int = Field(..., description="분")
    recipe: str = Field(..., description="레시피")
