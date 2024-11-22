from app.application.error import ErrorCode
from app.env_validator import get_settings
from aiohttp import ClientSession
from app.application.response import APIError

settings = get_settings()


class GoogleRequestService:
    def __init__(self) -> None:
        self._request = ClientSession()

    async def validate_id_token(self, id_token: str) -> dict:
        async with self._request.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
        ) as response:
            data = await response.json()
            if not data.get("aud") == settings.GOOGLE_CLIENT_ID:
                raise APIError(
                    status_code=400,
                    message="Invalid ID Token.",
                    error_code=ErrorCode.INVALID_GOOGLE_CODE,
                    error_data={
                        "user_message": "구글 로그인에 실패했습니다. 다시 시도해주세요.",
                    },
                )
            if not data.get("azp") == data.get("azp", "_DUMMY_AZP_DATA"):
                raise APIError(
                    status_code=400,
                    message="Invalid ID Token.",
                    error_code=ErrorCode.INVALID_GOOGLE_CODE,
                    error_data={
                        "user_message": "구글 로그인에 실패했습니다. 다시 시도해주세요.",
                    },
                )
            return data
