from dependency_injector import containers, providers

from app.auth.containers import AuthContainer
from app.google.containers import GoogleContainer


class AppContainers(containers.DeclarativeContainer):
    google: "GoogleContainer" = providers.Container(GoogleContainer)
    auth: "AuthContainer" = providers.Container(AuthContainer, google_service=google)
