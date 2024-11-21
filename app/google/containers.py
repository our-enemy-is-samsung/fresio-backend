from dependency_injector import containers, providers

from app.google.services import GoogleRequestService


class GoogleContainer(containers.DeclarativeContainer):
    service: GoogleRequestService = providers.Factory(GoogleRequestService)
