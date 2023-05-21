import typing as t

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware import Middleware

from sqlalchemy.ext.asyncio import create_async_engine

from brew_scout import TITLE, DESCRIPTION, VERSION
from brew_scout.vars import get_async_engine, set_async_engine
from .settings import AppSettings, SETTINGS_KEY
from ..apis.v1.health import router as health

API_PREFIX = "/api/v1"


def setup_app(settings: AppSettings) -> FastAPI:
    if not get_async_engine():
        engine = create_async_engine(settings.database_dsn, echo=settings.debug)
        set_async_engine(engine)
    
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
        title=TITLE,
        version=VERSION,
        description=DESCRIPTION,
        middleware=middlewares,
        default_response_class=ORJSONResponse,
        **{SETTINGS_KEY: settings}  # type: ignore
    )

    app = register_routers(app)

    return app


def add_origins() -> t.Sequence[str]:
    return ("http://localhost:9090", "http://0.0.0.0:9090")


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(health, prefix=f"{API_PREFIX}", tags=["health"])

    return app