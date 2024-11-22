from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class Match(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    match_type: str = Field(..., description="매치 타입 (single: 단식, double: 복식)")
    student1: list[str] = Field(..., description="학생1")
    student2: list[str] = Field(..., description="학생2")
