from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class VerificationCode(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    email: Indexed(str) = Field(..., description="이메일")
    user_id: Indexed(str) = Field(..., description="유저 ID")
    code: Indexed(str) = Field(..., description="인증 코드")  # @sen.go.kr
