from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncEngine

async_engine_var: ContextVar[AsyncEngine] = ContextVar("async_engine")


def get_async_engine() -> AsyncEngine | None:
    try:
        return async_engine_var.get()
    except LookupError:
        return None


def set_async_engine(engine: AsyncEngine) -> None:
    async_engine_var.set(engine)
