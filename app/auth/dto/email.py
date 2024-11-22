from typing import Annotated

from pydantic import EmailStr, StringConstraints, Field

from app.application.pydantic_model import BaseSchema
from app.env_validator import get_settings

settings = get_settings()

SenEmail = Annotated[
    EmailStr,
    StringConstraints(
        pattern=f"^[a-zA-Z0-9_.+-]+@(sen\.go\.kr|{settings.ADMIN_EMAIL_HOST})$"
    ),
]


class EmailVerificationRequestDTO(BaseSchema):
    email: SenEmail = Field(..., description="교육청 이메일 주소")


class EmailVerificationDTO(BaseSchema):
    session_id: str = Field(..., description="세션 ID")
    code: str = Field(..., description="인증 코드")
