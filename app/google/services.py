import os
from aiohttp import ClientSession
from app.application.response import APIError
from app.env_validator import get_settings
from app.logger import use_logger

import aiogoogle.excs
from aiogoogle import Aiogoogle, auth as aiogoogle_auth
from app.utils.string import GoogleScope

settings = get_settings()
logger = use_logger("google_service")
SERVER_STATE = os.urandom(32).hex()
logger.debug(f"Google Oauth2 Server state: {SERVER_STATE}")


class GoogleRequestService:
    def __init__(self) -> None:
        self.__server_state = SERVER_STATE

        self.__google_credentials = aiogoogle_auth.creds.ClientCreds(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=[
                GoogleScope["userinfo.email"],
                GoogleScope["userinfo.profile"],
                GoogleScope["docs"],
                GoogleScope["drive"],
                GoogleScope["drive.readonly"],
                GoogleScope["spreadsheets"],
            ],
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
        self._google_client = Aiogoogle(
            client_creds=self.__google_credentials,
        )
        self._request = ClientSession()

    def get_server_state(self) -> str:
        return self.__server_state

    async def get_authorization_url(self) -> str:
        return self._google_client.oauth2.authorization_url(
            state=self.__server_state,
            access_type="offline",
            include_granted_scopes=True,
            prompt="consent",
        )

    async def fetch_user_credentials(self, code: str) -> dict:
        return await self._google_client.oauth2.build_user_creds(
            grant=code, client_creds=self.__google_credentials
        )

    async def fetch_user_info(self, user_credentials: dict) -> dict:
        return await self._google_client.oauth2.get_me_info(
            user_creds=user_credentials,
        )
