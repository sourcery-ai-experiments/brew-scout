import dataclasses as dc
from collections import abc

from ..dal.shop import CoffeeShopRepository
from ..dal.models.shops import CoffeeShopModel


@dc.dataclass(slots=True, repr=True, frozen=True)
class CoffeeShopService:
    coffee_shop_repository: CoffeeShopRepository

    async def get_coffee_shops(self) -> abc.Sequence[CoffeeShopModel]:
        return await self.coffee_shop_repository.get_all()

    async def get_coffee_shops_for_city(self, city_name: str) -> abc.Sequence[CoffeeShopModel]:
        return await self.coffee_shop_repository.get_by_city_name(city_name)
