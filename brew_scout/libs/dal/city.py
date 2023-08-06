import typing as t
import dataclasses as dc
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession


@dc.dataclass(slots=True, repr=False)
class CityRepository:
    db: AsyncSession

    async def get_all(self) -> t.Sequence[str]:
        print(self.db)
        await asyncio.sleep(5)
        return {str(i) for i in range(3)}