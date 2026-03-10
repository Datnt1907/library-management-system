import contextlib
from collections.abc import AsyncIterator
from typing import TypedDict

from fastapi import FastAPI

from source.api import router
from source.config import settings
from source.exception_handlers import add_exception_handlers
from source.health.endpoints import router as health_router
from source.kit.db.postgres import (
    AsyncEngine,
    AsyncSessionMaker,
    create_async_sessionmaker,
)
from source.logging import configure as configure_logging
from source.postgres import AsyncSessionMiddleware, create_async_engine


class State(TypedDict):
    async_engine: AsyncEngine
    async_sessionmaker: AsyncSessionMaker


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async_engine = create_async_engine("app")
    async_sessionmaker = create_async_sessionmaker(async_engine)

    yield {"async_engine": async_engine, "async_sessionmaker": async_sessionmaker}
    await async_engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="My Library Management", lifespan=lifespan)
    if not settings.is_testing():
        app.add_middleware(AsyncSessionMiddleware)

    add_exception_handlers(app)

    app.include_router(health_router)

    app.include_router(router)
    return app


configure_logging()
app = create_app()
