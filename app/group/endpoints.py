import aiogoogle.excs
import tortoise
from dependency_injector.wiring import inject, Provide

import random
from fastapi import APIRouter, Depends, Request
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError
from app.auth.dto.auth import AuthVerifyDTO
from app.auth.schema.string import AuthorizationURLSchema
from app.containers import AppContainers
from app.google.services import GoogleRequestService

from app.user.entities import User
from app.user.entities.user import GoogleCredential

router = APIRouter(
    prefix="/group",
    tags=["Group"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class GroupEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.get("/list", description="그룹 목록을 반환합니다.")
    @inject
    async def get_team_list(self):
        ...

    @router.get("/{group_id}/list", description="그룹에 있는 서브 그룹 목록을 반환합니다.")
    @inject
    async def get_sub_group_list(self):
        ...

    @router.get("/{group_id}/{subgroup_id}/list", description="하위 그룹에 있는 학생을 반환합니다.")
    @inject
    async def get_student_list(self):
        ...






