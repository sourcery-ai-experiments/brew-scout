from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from brew_scout.vars import get_async_session
from ..dal.city import CityRepository


def city_repository_factory(db: AsyncSession = Depends(get_async_session)):
    return CityRepository(db)