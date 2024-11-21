from pydantic import Field

from app.application.pydantic_model import BaseSchema
from enum import Enum


class UserLoginRequestType(str, Enum):
    LOGIN = "login"
    SIGNUP = "signup"


class UserLoginResponse(BaseSchema):
    request_type: UserLoginRequestType = Field(
        ..., description="실행결과 (login: 로그인, signup: 회원가입/인증해야함)"
    )
    access_token: str = Field(..., description="JWT Access Token")
