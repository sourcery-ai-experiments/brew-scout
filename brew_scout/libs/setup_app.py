import typing as t
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware import Middleware

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from brew_scout import MODULE_NAME, DESCRIPTION, VERSION
from .settings import AppSettings, SETTINGS_KEY
from ..apis.v1.base import router as router_v1

API_PREFIX = "/api/v1"


def setup_app(settings: AppSettings) -> FastAPI:
    # if not get_async_engine():
        # engine = create_async_engine(settings.database_dsn, echo=settings.debug)
        # set_async_engine(engine)
    @asynccontextmanager
    async def app_lifespan(app: FastAPI) -> t.AsyncIterator[None]:
        engine = create_async_engine(settings.database_dsn, echo=settings.debug)
        async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        app.state.async_session_factory = async_session_factory

        try:
            yield
        finally:
            pass
    
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=add_origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    ]

    app = FastAPI(
        title=MODULE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        middleware=middlewares,
        lifespan=app_lifespan,
        default_response_class=ORJSONResponse,
        **{SETTINGS_KEY: settings}  # type: ignore
    )

    app.include_router(router_v1)

    return app


def add_origins() -> t.Sequence[str]:
    return ("http://localhost:9090", "http://0.0.0.0:9090")
