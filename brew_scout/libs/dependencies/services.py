from fastapi import Depends

from .repositories import city_repository_factory
from ..services.city import CityService
from ..dal.city import CityRepository


async def city_service_factory(
    city_repository: CityRepository = Depends(city_repository_factory)
) -> CityService:
    return CityService(city_repository)
