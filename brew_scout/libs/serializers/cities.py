from pydantic import BaseModel


class CountryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CityOut(BaseModel):
    id: int
    name: str
    country: CountryOut

    class Config:
        orm_mode = True
