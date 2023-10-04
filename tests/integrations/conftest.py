import pytest

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from brew_scout.libs.settings import AppSettings
from brew_scout.libs.setup_app import setup_app, configure_db_session_factory
from brew_scout.vars import set_async_session

from tests.conftest import AsyncScopedSession


@pytest.fixture()
async def async_app(pg_conf):
    settings = AppSettings(
        database_dsn=f"postgresql+asyncpg://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{pg_conf['db']}",
        telegram_api_url="https://telegram.org",
        telegram_api_token="token",
    )
    app = setup_app(settings)

    async with LifespanManager(app, startup_timeout=None):
        yield app


@pytest.fixture()
async def configure_session(pg_conf, create_db):
    engine = create_async_engine(
        f"postgresql+asyncpg://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{pg_conf['db']}"
    )
    configure_db_session_factory(engine, AsyncScopedSession)

    try:
        yield
    finally:
        await AsyncScopedSession.remove()
        await engine.dispose()


@pytest.fixture()
def app(async_app, configure_session):
    set_async_session(AsyncScopedSession)
    return async_app


@pytest.fixture()
async def client(app):
    async with AsyncClient(app=app, base_url="http://base") as client:
        yield client


@pytest.fixture()
def db_session(app):
    return AsyncScopedSession
