from fastapi import Depends

from .common import settings_factory
from ..settings import AppSettings
from ..clients.telegram import TelegramClinet
from ..clients.geo import GeoClient


def telegram_client_factory(settings: AppSettings = Depends(settings_factory)) -> TelegramClinet:
    return TelegramClinet(api_url=f"{settings.telegram_api_url}{settings.telegram_api_token}")


def geo_client_factory() -> GeoClient:
    return GeoClient()
