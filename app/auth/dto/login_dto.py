from pydantic import Field

from app.application.pydantic_model import BaseSchema


class GoogleLoginDTO(BaseSchema):
    id_token: str = Field(
        ..., description="Google Callback Code", examples=["4/0AX4XfW"]
    )