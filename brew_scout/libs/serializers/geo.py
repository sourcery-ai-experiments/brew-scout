from collections import abc

from pydantic import BaseModel


class Address(BaseModel):
    city: str | None
    country: str
    country_code: str
    municipality: str | None


class NominatimResponse(BaseModel):
    place_id: int
    osm_type: str
    osm_id: int
    lat: float
    lon: float
    display_name: str
    address: Address
    boundingbox: abc.Sequence[float]
