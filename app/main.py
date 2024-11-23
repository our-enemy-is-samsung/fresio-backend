from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import generate_config, Tortoise
from tortoise.contrib.fastapi import RegisterTortoise
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.application.response import APIError
from app.logger import use_logger
from app.env_validator import get_settings
from app.containers import AppContainers

from app.user.entities import User

from app.auth.endpoints import router as auth_router
from app.home.endpoints import router as home_router
from app.recipe.endpoints import router as recipe_router
from app.refrigerator.endpoints import router as refrigerator_router
from app.timer.endpoints import router as timer_router
from app.hardware.endpoints import router as hardware_router

logger = use_logger("bootstrapper")
settings = get_settings()

TEST_USER_UUID = "17fca8cb-b391-4aa6-8338-976a956fa788"


def bootstrap() -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> None:
        logger.info("Starting application")
        config = generate_config(
            settings.DATABASE_URI,
            app_modules={"models": ["app.user.entities", "app.hardware.entities"]},
            testing=settings.APP_ENV == "testing",
            connection_label="models",
        )
        application.container = container

        container.wire(
            modules=[
                __name__,
                "app.auth.endpoints",
                "app.home.endpoints",
                "app.recipe.endpoints",
                "app.refrigerator.endpoints",
                "app.timer.endpoints",
                "app.hardware.endpoints",
            ]
        )
        logger.info("Container Wiring complete")
        async with RegisterTortoise(
            app=application,
            config=config,
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            logger.info("Tortoise ORM registered")
            yield
        logger.info("Shutting down application")
        await Tortoise.close_connections()
        logger.info("Tortoise ORM connections closed")
        logger.info("Application shutdown complete")

    app = FastAPI(
        title="Fresio API",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url=None,
        debug=settings.APP_ENV == "development",
    )
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return app


container = AppContainers()
server = bootstrap()

server.include_router(auth_router)
server.include_router(home_router)
server.include_router(recipe_router)
server.include_router(refrigerator_router)
server.include_router(timer_router)
server.include_router(hardware_router)
