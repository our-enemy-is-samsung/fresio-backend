import uuid
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError
from app.auth.dto import auth
from app.auth.services import AuthService
from app.containers import AppContainers

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
        description="디바이스 로그인",
        response_model=APIResponse[dict],
    )
    @inject
    async def google_login(
        self,
        data: auth.DeviceLoginDTO,
        auth_service: "AuthService" = Depends(Provide[AppContainers.auth.service]),
    ) -> APIResponse[dict]:
        entity = await auth_service.get_from_device(data.device_id)
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

    @router.post(
        "/register",
        description="로그인",
        response_model=APIResponse[dict],
    )
    @inject
    async def google_signup(
        self,
        data: auth.DeviceRegisterDTO,
        auth_service: "AuthService" = Depends(Provide[AppContainers.auth.service]),
    ) -> APIResponse[dict]:
        entity = await auth_service.get_from_device(data.device_id)
        if entity:
            raise APIError(
                status_code=400,
                message="User already exists.",
                error_code=ErrorCode.USER_ALREADY_EXISTS,
            )
        user = await User.create(
            id=uuid.uuid4(),
            name=data.name,
            device_id=data.device_id,
            meal_type=data.meal_type,
            food_check=auth_service.analyze_average_intake(data.food_check).name,
        )
        access_token = await auth_service.create_access_token(str(user.id))
        return APIResponse[dict](
            status="success",
            message="User registered successfully",
            data={"access_token": access_token},
        )
