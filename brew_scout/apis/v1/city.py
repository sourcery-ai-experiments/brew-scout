import typing as t
from fastapi import APIRouter, Depends

from ...libs.dependencies.common import on_async_session_trx_factory
from ...libs.dependencies.services import city_service_factory
from ...libs.services.city import CityService


router = APIRouter(tags=["Cities"])


@router.get("/cities", dependencies=[Depends(on_async_session_trx_factory)])
async def get_cities(service: CityService = Depends(city_service_factory)) -> t.Sequence[str]:
    return await service.get_cities()