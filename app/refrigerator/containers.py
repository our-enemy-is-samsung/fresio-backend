from dependency_injector import containers, providers

from app.refrigerator.services import RefrigeratorService


class RefrigeratorContainer(containers.DeclarativeContainer):
    service: "RefrigeratorService" = providers.Factory(RefrigeratorService)
