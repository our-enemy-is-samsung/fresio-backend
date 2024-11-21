from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field

from app.application.pydantic_model import BaseSchema


class GoogleCredential(BaseSchema):
    refresh_token: str = Field(..., description="구글 OAuth2 refresh token")
    access_token: str = Field(..., description="구글 OAuth2 access token")
    access_token_expires_at: datetime = Field(
        ..., description="구글 OAuth2 access token 만료 시간"
    )
    refresh_count: int = Field(50, description="구글 OAuth2 refresh 횟수")


class User(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: Indexed(str) = Field(..., description="사용자 이름")
    email: Indexed(str, unique=True) = Field(
        ..., description="사용자 이메일"
    )  # 이메일은 유니크해야 할 것 같아서 unique 인덱스 추가
    sen_email: str | None = Field(None, description="교육청 이메일")
    picture: Indexed(str) = Field(..., description="사용자 프로필 사진")
    google_credential: GoogleCredential = Field(..., description="구글 OAuth2 정보")
    verified: bool = Field(False, description="공직자 이메일 인증 여부")
