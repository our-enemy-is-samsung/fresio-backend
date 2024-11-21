from pydantic import Field

from app.application.pydantic_model import BaseSchema


class AuthVerifyDTO(BaseSchema):
    state: str = Field(..., description="서버에서 제공한 state 값")
    code: str = Field(..., description="구글 로그인 후 받은 code 값")
