from dependency_injector import containers, providers

from app.bracket.services import BracketService


class BracketContainer(containers.DeclarativeContainer):
    service: BracketService = providers.Factory(BracketService)
