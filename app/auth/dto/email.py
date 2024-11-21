from typing import Annotated

from pydantic import EmailStr, StringConstraints, Field

from app.application.pydantic_model import BaseSchema

SenEmail = Annotated[
    EmailStr, StringConstraints(pattern=r"^[a-zA-Z0-9_.+-]+@gmail\.com$")
]


class EmailVerificationRequestDTO(BaseSchema):
    email: SenEmail = Field(..., description="교육청 이메일 주소")


class EmailVerificationDTO(BaseSchema):
    session_id: str = Field(..., description="세션 ID")
    code: str = Field(..., description="인증 코드")
