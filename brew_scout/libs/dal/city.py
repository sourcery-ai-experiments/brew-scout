import dataclasses as dc
import typing as t
from collections import abc

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .models.cities import CityModel


CityId: t.TypeAlias = int


@dc.dataclass(slots=True, repr=False)
class CityRepository:
    db: AsyncSession

    async def get_one_or_none(self, city_id: CityId) -> CityModel | None:
        q = select(CityModel).options(joinedload(CityModel.country)).where(CityModel.id == city_id)

        result = await self.db.scalars(q)

        return result.one_or_none()

    async def get_all(self) -> abc.Sequence[CityModel]:
        q = select(CityModel).options(joinedload(CityModel.country))

        result = await self.db.scalars(q)

        return result.all()
