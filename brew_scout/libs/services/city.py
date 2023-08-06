import typing as t
import dataclasses as dc

from ..dal.city import CityRepository


@dc.dataclass(slots=True, repr=False)
class CityService:
    city_repository: CityRepository

    async def get_cities(self) -> t.Sequence[str]:
        return await self.city_repository.get_all()
