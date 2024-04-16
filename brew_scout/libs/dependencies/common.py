import typing as t
from collections import abc

from aiohttp import ClientSession

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis
from starlette.background import BackgroundTasks
from starlette.requests import Request

from ..settings import AppSettings, SETTINGS_KEY
from ..managers import db_manager, rds_manager


T = t.TypeVar("T")
P = t.ParamSpec("P")
BackgroundRunner = abc.Callable[..., abc.Awaitable[None]]


def settings_factory(request: Request) -> AppSettings:
    return request.app.extra[SETTINGS_KEY]


def client_session_factory(request: Request) -> abc.Callable[..., ClientSession]:
    return request.app.state.client_session_getter


async def get_db_session() -> t.AsyncGenerator[AsyncSession, None]:
    async with db_manager.session() as session:
        yield session


async def get_rds_session() -> abc.AsyncGenerator[Redis, None]:
    async with rds_manager.session() as redis_client:
        yield redis_client


async def background_runner_factory(request: Request, background_tasks: BackgroundTasks) -> BackgroundRunner:
    _ = await request.json()
    run_now = bool(request.query_params.get("run_now", False))

    async def background_runner(func: abc.Callable[P, abc.Awaitable[T]], *args: P.args, **kwargs: P.kwargs) -> None:
        if run_now:
            await func(*args, **kwargs)
            return

        # Run the function in the background
        background_tasks.add_task(func, *args, **kwargs)
        return

    return background_runner
