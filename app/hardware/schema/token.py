from pydantic import Field

from app.application.pydantic_model import BaseSchema


class RegisteredHardwareTokenSchema(BaseSchema):
    device_token: str = Field(..., description="디바이스 토큰")
