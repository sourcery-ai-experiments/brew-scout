import dataclasses as dc
import typing as t
from collections import abc

from brew_scout.libs.clients.geo import GeoClient

from brew_scout.libs.serializers.geo import NominatimResponse


@dc.dataclass(frozen=True, slots=True, repr=False)
class GeoService:
    client: GeoClient
    default_language: str = "en"

    async def find_city_from_coordinates(self, latitude: float, longitude: float) -> t.Any:
        raw_result = await self._request(latitude, longitude)
        result = NominatimResponse.parse_obj(raw_result)

        return result.boundingbox

    async def find_nearest_coffee_shops(self) -> abc.Sequence[str]:
        ...

    async def _request(self, latitude: float, longitude: float) -> abc.Mapping[str, t.Any]:
        async with self.client() as geolocator:
            location = await geolocator.reverse((latitude, longitude), language=self.default_language)

            return location.raw
