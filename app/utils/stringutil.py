import secrets
import string
from urllib.parse import urlencode
from app.env_validator import get_settings

settings = get_settings()


class GoogleScope:
    BASE_URL = "https://www.googleapis.com/auth"

    def __class_getitem__(cls, key: str) -> str:
        return f"{cls.BASE_URL}/{key}"


def generate_google_oauth_url(
    client_id: str = settings.GOOGLE_CLIENT_ID,
    redirect_uri: str = "http://localhost:8080/auth/_test_callback",
) -> str:
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "online",
        "prompt": "consent",
    }

    return f"{base_url}?{urlencode(params)}"


def generate_secret_token() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(30))
