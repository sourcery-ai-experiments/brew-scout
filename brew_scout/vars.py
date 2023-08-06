from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

async_session_var: ContextVar[AsyncSession] = ContextVar("async_session")


def get_async_session() -> AsyncSession:
    return async_session_var.get()


def set_async_session(session: AsyncSession) -> None:
    async_session_var.set(session)
