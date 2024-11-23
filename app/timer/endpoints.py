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
from app.timer.dto.create import CookTimerCreateSchema
from app.timer.dto.update import CookTimerUpdateSchema, CookTimerStepUpdateSchema
from app.timer.schema.cooktimer_detail import CookTimerDetailSchema, CookTimerStepSchema
from app.timer.schema.cooktimer_preview import CookTimerPreviewSchema

from app.user.entities import User

router = APIRouter(
    prefix="/timer",
    tags=["Timer"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class TimerEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.get(
        "/list",
        description="타이머 조회",
    )
    @inject
    async def get_timer(
        self,
        _user: User = Depends(get_current_user_entity),
    ) -> APIResponse[list[CookTimerPreviewSchema]]:
        return APIResponse(
            message="레시피 상세 조회",
            data=[
                CookTimerPreviewSchema(
                    id=uuid.uuid4(),
                    name="토마토",
                    time=33,
                )
            ],
        )

    @router.get(
        "/{timer_id}",
        description="타이머 상세 조회",
    )
    async def fetch_timer(self, timer_id: str) -> APIResponse[CookTimerDetailSchema]:
        return APIResponse(
            message="타이머 상세 조회",
            data=CookTimerDetailSchema(
                id=uuid.uuid4(),
                name="토마토",
                color=TimerColor.RED,
                emoji="🍅",
                steps=[
                    CookTimerStepSchema(
                        time=33,
                        recipe="레시피",
                    ),
                    CookTimerStepSchema(
                        time=33,
                        recipe="레시피",
                    ),
                ],
            ),
        )

    @router.post(
        "/{timer_id}/remote",
        description="타이머 원격 제어 (프레시오로 타이머 전송하기)",
    )
    async def remote_timer(
        self,
        timer_id: str,
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 원격 제어",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.get(
        "/{timer_id}/delete",
        description="타이머 삭제",
    )
    async def delete_timer(
        self, timer_id: str
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 삭제",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.post(
        "/{timer_id}/edit",
        description="타이머 생성",
    )
    async def edit_timer(
        self,
        timer_id: str,
        data: CookTimerUpdateSchema,
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 생성",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.post("/{timer_id}/step/add", description="타이머 스탭 추가")
    async def add_timer_step(
        self, timer_id: str, data: CookTimerStepUpdateSchema
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 스탭 추가",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.post(
        "/{timer_id}/step/{step_index}/edit",
        description="타이머 스탭 수정",
    )
    async def edit_timer_step(
        self,
        timer_id: str,
        step_index: int,
        data: CookTimerStepUpdateSchema,
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 스탭 수정",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.get(
        "/{timer_id}/step/{step_index}/delete",
        description="타이머 스탭 삭제",
    )
    async def delete_timer_step(
        self,
        timer_id: str,
        step_index: int,
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 스탭 삭제",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )

    @router.post(
        "/create",
        description="타이머 생성하기",
    )
    async def create_timer(
        self,
        data: CookTimerCreateSchema,
    ) -> APIResponse[SuccessfulEntityResponse]:
        return APIResponse(
            message="타이머 생성하기",
            data=SuccessfulEntityResponse(
                entity_id=uuid.uuid4(),
            ),
        )
