from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext

from app.application.response import APIError
from app.application.error import ErrorCode
from app.auth.dto.auth import FoodCheckFormDTO, FoodCheckEnum
from app.env_validator import get_settings
from app.logger import use_logger

from app.user.entities import User
from app.application.typevar import USER_ID

logger = use_logger("auth_service")
settings = get_settings()


async def get_phone_by_token(token: str) -> str:
    payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    return payload.get("phone")


class AuthService:
    def __init__(self) -> None:
        self.hashed_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def get_from_device(device_id: str) -> User | bool:
        entity = await User.get_or_none(device_id=device_id)
        if not entity:
            return False
        return entity

    def create_nonce(self, entity_id: str, salt: str) -> str:
        nonce_content = (
            salt[0] + "73" + entity_id[:6] + salt[2:4] + "2" + entity_id[7:10]
        )
        return self.hashed_context.hash(nonce_content)

    def check_nonce(self, entity_id: str, salt: str, nonce: str) -> bool:
        nonce_content = (
            salt[0] + "73" + entity_id[:6] + salt[2:4] + "2" + entity_id[7:10]
        )
        return self.hashed_context.verify(nonce_content, nonce)

    def synchronous_create_access_token(self, entity_id: str) -> str:
        hash_nonce = self.create_nonce(entity_id, settings.JWT_SECRET_KEY[2:8])
        encoded_jwt = jwt_encode(
            {"uid": entity_id, "hn": hash_nonce},
            settings.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        return encoded_jwt

    async def create_access_token(self, entity_id: str) -> str:
        return self.synchronous_create_access_token(entity_id)

    async def get_user_id_from_token(self, token: str) -> USER_ID:
        payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        check_hash = self.create_nonce(payload.get("uid"), settings.JWT_SECRET_KEY[2:8])
        if check_hash != payload.get("hn"):
            raise APIError(
                status_code=400,
                message="Token validation failed",
                error_code=ErrorCode.INVALID_ACCESS_TOKEN,
            )
        return payload.get("uid")

    @staticmethod
    def get_access_token_payload(token: str) -> tuple[str, str] or None:
        try:
            payload = jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            return payload.get("uid"), payload.get("hn")
        except PyJWTError:
            return None

    @staticmethod
    def analyze_average_intake(food_check_data: FoodCheckFormDTO) -> FoodCheckEnum:
        status_scores = {
            FoodCheckEnum.too_much: 3,
            FoodCheckEnum.just_right: 2,
            FoodCheckEnum.too_little: 1,
        }

        total_score = sum(
            [
                status_scores[food_check_data.food_check_pasta],
                status_scores[food_check_data.food_check_pizza],
                status_scores[food_check_data.food_check_cutlet],
                status_scores[food_check_data.food_check_ramen],
                status_scores[food_check_data.food_check_bibimbap],
            ]
        )

        average_score = total_score / 5

        if average_score > 2.3:
            return FoodCheckEnum.too_much
        elif average_score < 1.7:
            return FoodCheckEnum.too_little
        else:
            return FoodCheckEnum.just_right
