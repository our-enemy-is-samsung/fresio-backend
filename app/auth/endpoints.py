import aiogoogle.excs
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.authorization import get_current_user_id
from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError, SuccessfulEntityResponse
from app.auth.dto import login_dto
from app.auth.schema.string import AuthorizationURLSchema
from app.auth.schema.user import UserLoginResponse, UserLoginRequestType
from app.auth.services import AuthService
from app.containers import AppContainers
from app.google.services import GoogleRequestService

from app.user.entities import User

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class AuthEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.post(
        "/login",
        description="구글 로그인",
        response_model=APIResponse[dict],
    )
    @inject
    async def google_login(
        self,
        data: login_dto.GoogleLoginDTO,
        google_service: "GoogleRequestService" = Depends(
            Provide[AppContainers.google.service]
        ),
        auth_service: "AuthService" = Depends(Provide[AppContainers.auth.service]),
    ) -> APIResponse[dict]:
        google_user_data = await google_service.validate_id_token(data.id_token)
        entity = await auth_service.get_from_credential(
            "email::" + google_user_data["email"]
        )
        if not entity:
            raise APIError(
                status_code=400,
                message="User not found.",
                error_code=ErrorCode.USER_NOT_FOUND,
            )
        access_token = await auth_service.create_access_token(str(entity.id))
        return APIResponse[dict](
            status="success",
            message="User logged in successfully",
            data={"access_token": access_token},
        )
