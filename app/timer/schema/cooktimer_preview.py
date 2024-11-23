from uuid import UUID

from pydantic import Field

from app.application.pydantic_model import BaseSchema
from app.application.typevar import UNICODE_EMOJI


class CookTimerPreviewSchema(BaseSchema):
    id: UUID = Field(..., description="타이머 ID")
    emoji: UNICODE_EMOJI = Field(..., description="타이머 이모지")
    name: str = Field(..., description="타이머 이름")
    step_count: int = Field(..., description="작업 단계 수")
    time: int = Field(..., description="총 소요 시간 (분)")
