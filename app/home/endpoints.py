import uuid
from datetime import datetime
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.authorization import get_current_user_entity
from app.application.error import ErrorCode
from app.application.response import APIResponse, APIError
from app.auth.dto import auth
from app.auth.services import AuthService
from app.containers import AppContainers
from app.enums.cook_difficulty import CookDifficulty
from app.google.services import GoogleRequestService
from app.home.schema.expiring_food import ExpiringFoodItemSchema
from app.home.schema.recommend import (
    RecommendationSchema,
    CookingRecommendSchema,
    ServiceRecommendSchema,
)
from app.home.schema.section import (
    PersonalizedRecommendationSchema,
    PersonalizedRecommendationSectionSchema,
    PersonalizedRecommendationRecipeSchema,
)

from app.user.entities import User

router = APIRouter(
    prefix="/home",
    tags=["Home"],
    responses={404: {"description": "Not found"}},
)
limiter = Limiter(key_func=get_remote_address)


@cbv(router)
class HomeEndpoint:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @router.get("/expiring-foods", description="홈화면 소비기한 임박 쟤료 UI")
    @inject
    async def get_expiring_foods(
        self, _user: User = Depends(get_current_user_entity)
    ) -> APIResponse[list[ExpiringFoodItemSchema]]:

        return APIResponse(
            message="success",
            data=[
                ExpiringFoodItemSchema(
                    id=uuid.uuid4(),
                    icon="🍅",
                    name="토마토",
                    expired_at=datetime.now(),
                    quantity=3,
                )
            ],
        )

    @router.get("/recommendation", description="홈화면 추천 레시피, 서비스 UI")
    async def get_recommendation(
        self, _user: User = Depends(get_current_user_entity)
    ) -> APIResponse[RecommendationSchema]:
        return APIResponse(
            message="success",
            data=RecommendationSchema(
                recipe=CookingRecommendSchema(
                    recipie_id=uuid.uuid4(),
                    recommend_title="서늘한 저녁 이 음식은 어떤가요?",
                    title="바나나 버터구이 프렌치 토스트",
                    image_url="https://image_url.com",
                    difficulty=CookDifficulty.EASY,
                    estimated_time=10,
                ),
                service=ServiceRecommendSchema(
                    recommend_id=uuid.uuid4(),
                    ui_small_top_text="가장 많이 찾는",
                    ui_main_text="라면 타이머 실행하기",
                    internal_deep_link="timer/index",
                ),
            ),
        )

    @router.get(
        "/recommendation/section",
        description="홈화면 추천 미니 추천 레시피",
    )
    async def get_recommendation_section(
        self, _user: User = Depends(get_current_user_entity)
    ) -> APIResponse[PersonalizedRecommendationSchema]:
        return APIResponse(
            message="success",
            data=PersonalizedRecommendationSchema(
                sections=[
                    PersonalizedRecommendationSectionSchema(
                        section_name="서늘한 저녁 이 음식은 어떤가요?",
                        recipes=[
                            PersonalizedRecommendationRecipeSchema(
                                recipe_id=uuid.uuid4(),
                                ingredients=["바나나", "버터", "토스트"],
                                name="바나나 버터구이 프렌치 토스트",
                                difficulty=CookDifficulty.EASY,
                                estimated_time=10,
                            )
                        ],
                    )
                ]
            ),
        )
