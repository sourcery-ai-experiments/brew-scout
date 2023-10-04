import dataclasses as dc
from collections import abc

from sqlalchemy import select, LABEL_STYLE_TABLENAME_PLUS_COL
from sqlalchemy.orm import joinedload

from .models.shops import CoffeeShopModel
from .models.cities import CityModel
from ...vars import get_async_session


@dc.dataclass(slots=True, repr=False)
class CoffeeShopRepository:
    # db: AsyncSession

    async def get_all(self) -> abc.Sequence[CoffeeShopModel]:
        db = get_async_session()
        q = (
            select(CoffeeShopModel)
            .options(joinedload(CoffeeShopModel.city).joinedload(CityModel.country))
            .set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL)
        )

        result = await db.scalars(q)

        return result.all()

    async def get_by_city_name(self, city_name: str) -> abc.Sequence[CoffeeShopModel]:
        db = get_async_session()
        q = select(CoffeeShopModel).options(joinedload(CoffeeShopModel.city)).where(CityModel.name.ilike(city_name))

        result = await db.scalars(q)

        return result.all()
