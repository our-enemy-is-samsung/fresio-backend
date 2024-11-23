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
from app.google.services import GoogleRequestService

from app.user.entities import User

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class RecipieEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.get(
        "/{recipe_id}",
        description="레시피 상세 조회",
    )
    @inject
    async def get_recipe(
        self,
        recipe_id: str,
    ) -> APIResponse[dict]:
        return APIResponse[dict](
            status="success",
            message="레시피 상세 조회",
            data={"recipe_id": recipe_id},
        )
