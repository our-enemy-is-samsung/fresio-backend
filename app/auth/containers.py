from dependency_injector import containers, providers
from typing import TYPE_CHECKING

from app.auth.services import AuthService

if TYPE_CHECKING:
    from app.google.services import GoogleRequestService


class AuthContainer(containers.DeclarativeContainer):
    google_service: "GoogleRequestService" = providers.Dependency()
    service: "AuthService" = providers.Factory(AuthService)
