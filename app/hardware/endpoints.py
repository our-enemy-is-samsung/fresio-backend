from uuid import UUID
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, Body, WebSocketDisconnect, WebSocket
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.authorization import get_current_user_entity
from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError
from app.containers import AppContainers
from app.hardware.entities import Hardware
from app.hardware.redis_session import RedisHardwareConnectionManager
from app.hardware.schema.token import RegisteredHardwareTokenSchema
from app.hardware.services import HardwareService

from app.user.entities import User

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class HardwareEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.post("/register-display", description="디스플레이 등록")
    @inject
    async def register_display(
        self,
        user: User = Depends(get_current_user_entity),
        device_id: str = Body(..., description="디스플레이 디바이스 ID", embed=True),
        hardware_service: "HardwareService" = Depends(
            Provide[AppContainers.hardware.service]
        ),
    ) -> APIResponse[RegisteredHardwareTokenSchema]:
        if user.display_hardware:
            raise APIError(
                status_code=400,
                message="Display already registered",
                error_code=ErrorCode.HARDWARE_ALREADY_REGISTERED,
            )
        device_token = await hardware_service.register_display(user, device_id)
        return APIResponse(
            message="디스플레이 등록 성공",
            data=RegisteredHardwareTokenSchema(device_token=device_token),
        )

    @router.post("/register-camera", description="카메라 등록")
    @inject
    async def register_camera(
        self,
        user: User = Depends(get_current_user_entity),
        device_id: str = Body(..., description="카메라 디바이스 ID", embed=True),
        hardware_service: "HardwareService" = Depends(
            Provide[AppContainers.hardware.service]
        ),
    ) -> APIResponse[RegisteredHardwareTokenSchema]:
        if user.camera_hardware:
            raise APIError(
                status_code=400,
                message="Camera already registered",
                error_code=ErrorCode.HARDWARE_ALREADY_REGISTERED,
            )
        device_token = await hardware_service.register_camera(user, device_id)
        return APIResponse(
            message="카메라 등록 성공",
            data=RegisteredHardwareTokenSchema(device_token=device_token),
        )


@router.websocket("/ws/{hardware_token}")
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    hardware_token: str,
    connection_manager: "RedisHardwareConnectionManager" = Depends(
        Provide[AppContainers.hardware.connection_manager]
    ),
):
    hardware_entity = await Hardware.get_or_none(token=hardware_token)
    if not hardware_entity:
        await websocket.close(code=1008, reason="Hardware not found")
        return

    await websocket.accept()
    await connection_manager.connect(
        str(hardware_entity.id), hardware_entity.user_id, hardware_entity.device_type
    )
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was:")
    except WebSocketDisconnect:
        await connection_manager.disconnect(
            hardware_entity.user_id, hardware_entity.device_type
        )
        await websocket.close()
