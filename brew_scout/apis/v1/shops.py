from collections import abc

from fastapi import APIRouter, Depends

from ...libs.dependencies.common import on_async_session_factory
from ...libs.dependencies.services import coffee_shop_service_factory
from ...libs.services.shop import CoffeeShopService
from ...libs.serializers.shops import CoffeeShopsOut
from ...libs.dal.models.shops import CoffeeShopModel


router = APIRouter(tags=["Coffee Shops"])


@router.get("/shops", response_model=abc.Sequence[CoffeeShopsOut], dependencies=[Depends(on_async_session_factory)])
async def get_shops(service: CoffeeShopService = Depends(coffee_shop_service_factory)) -> abc.Sequence[CoffeeShopModel]:
    return await service.get_coffee_shops()
