from pydantic import BaseModel, AnyHttpUrl

from .cities import CityOut


class CoffeeShopsOut(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    city: CityOut
    web_url: AnyHttpUrl

    class Config:
        orm_mode = True
