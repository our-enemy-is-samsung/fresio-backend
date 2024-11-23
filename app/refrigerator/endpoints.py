import uuid
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime
from datetime import timedelta

from app.application.authorization import get_current_user_entity
from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError, SuccessfulEntityResponse
from app.auth.dto import auth
from app.auth.services import AuthService
from app.containers import AppContainers
from app.enums.color import TimerColor
from app.google.services import GoogleRequestService
from app.refrigerator.dto.add import AddIngredientDTO
from app.refrigerator.entities import Ingredient
from app.refrigerator.schema.ingredient import IngredientSchema
from app.refrigerator.services import RefrigeratorService
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
        user: User = Depends(get_current_user_entity),
    ) -> APIResponse[list[IngredientSchema]]:
        user = await User.get(id=user.id).prefetch_related("refrigerator")
        ingredients = await user.refrigerator.all()
        return APIResponse(
            message="냉장고 재료 조회",
            data=[
                IngredientSchema(
                    id=item.id,
                    name=item.name,
                    created_at=item.created_at,
                    expired_at=item.expired_at,
                    quantity=item.quantity,
                    thumbnail_image=item.thumbnail_image,
                )
                for item in ingredients
            ],
        )

    @router.post(
        "/add",
        description="냉장고 재료 추가",
    )
    @inject
    async def add_ingredient(
        self,
        data: AddIngredientDTO,
        user: User = Depends(get_current_user_entity),
    ) -> APIResponse[SuccessfulEntityResponse]:
        last_2seen = datetime.now() + timedelta(days=2)
        new_ingredient = await Ingredient.create(
            id=uuid.uuid4(),
            name=data.name,
            created_at=datetime.now(),
            expired_at=last_2seen,
            quantity=data.quantity,
            icon=data.icon,
            items=data.items,
        )
        await user.refrigerator.add(new_ingredient)
        return APIResponse(message=q)
