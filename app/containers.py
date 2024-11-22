from dependency_injector import containers, providers

from app.auth.containers import AuthContainer
from app.bracket.containers import BracketContainer
from app.google.containers import GoogleContainer
from app.email.containers import EmailContainer


class AppContainers(containers.DeclarativeContainer):
    google: "GoogleContainer" = providers.Container(GoogleContainer)
    auth: "AuthContainer" = providers.Container(AuthContainer, google_service=google)
    email: "EmailContainer" = providers.Container(EmailContainer)
    bracket: "BracketContainer" = providers.Container(BracketContainer)
