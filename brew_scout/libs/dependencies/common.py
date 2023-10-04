import typing as t
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession

from brew_scout.vars import set_async_session
from ..settings import AppSettings, SETTINGS_KEY


def settings_factory(request: Request) -> AppSettings:
    return request.app.extra[SETTINGS_KEY]


async def on_async_session_factory(request: Request) -> t.AsyncIterator[AsyncSession]:
    async_session_factory = request.app.state.async_session_factory

    async with async_session_factory() as session:
        set_async_session(session)
        yield session
