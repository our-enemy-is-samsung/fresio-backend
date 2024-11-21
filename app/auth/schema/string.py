from pydantic import Field

from app.application.pydantic_model import BaseSchema


class AuthorizationURLSchema(BaseSchema):
    url: str = Field(..., description="구글 로그인 URL")
