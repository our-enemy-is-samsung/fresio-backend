from pydantic import Field
from app.application.pydantic_model import BaseSchema
from app.bracket.entities import Match


class BracketMatchSchema(BaseSchema):
    match_id: str = Field(..., description="매치 ID")
    match_type: str = Field(..., description="매치 타입 (single: 단식, double: 복식)")
    student1: list[str] = Field(..., description="학생1")
    student2: list[str] = Field(..., description="학생2")


class BracketMatchListSchema(BaseSchema):
    matches: list[BracketMatchSchema] = Field(..., description="매치 목록")
    unmatched_count: dict[str, int] = Field(..., description="미매칭 학생 수")


class SavedBracketMatchListSchema(BaseSchema):
    matches: list[Match] = Field(..., description="매치 목록")
