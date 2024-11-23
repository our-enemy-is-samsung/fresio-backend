import uuid
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.authorization import get_current_user_entity
from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError, SuccessfulEntityResponse
from app.auth.dto import auth
from app.auth.services import AuthService
from app.containers import AppContainers
from app.enums.color import TimerColor
from app.google.services import GoogleRequestService
from app.refrigerator.schema.ingredient import IngredientSchema
from app.timer.dto.create import CookTimerCreateSchema
from app.timer.dto.update import CookTimerUpdateSchema, CookTimerStepUpdateSchema
from app.timer.schema.cooktimer_detail import CookTimerDetailSchema, CookTimerStepSchema
from app.timer.schema.cooktimer_preview import CookTimerPreviewSchema

from app.user.entities import User

router = APIRouter(
    prefix="/refrigerator",
    tags=["Refrigerator"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class RefrigeratorEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.get(
        "/list",
        description="냉장고 재료 조회",
    )
    @inject
    async def get_ingredient(
        self,
        _user: User = Depends(get_current_user_entity),
    ) -> APIResponse[list[IngredientSchema]]:
        from datetime import datetime

        return APIResponse(
            message="냉장고 재료 조회",
            data=[
                IngredientSchema(
                    id=uuid.uuid4(),
                    name="토마토",
                    created_at=datetime.fromisoformat("2021-10-01T00:00:00"),
                    expired_at=datetime.fromisoformat("2021-10-01T00:00:00"),
                    quantity=1,
                    thumbnail_image="https://example.com/image",
                ),
            ],
        )
