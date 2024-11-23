from dependency_injector import containers, providers
from app.hardware.redis_session import RedisHardwareConnectionManager
from app.hardware.services import HardwareService


class HardwareContainer(containers.DeclarativeContainer):
    service: "HardwareService" = providers.Factory(HardwareService)
    connection_manager: "RedisHardwareConnectionManager" = providers.Factory(
        RedisHardwareConnectionManager
    )
