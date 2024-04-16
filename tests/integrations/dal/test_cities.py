import pytest

from brew_scout.libs.dal.city import CityRepository
from brew_scout.libs.dal.models.cities import CityModel
from brew_scout.libs.domains.cities import City


@pytest.fixture()
def repository(db_session):
    return CityRepository(CityModel, db_session)


@pytest.mark.parametrize(
    "some_city_latitude, some_city_longitude, expected_city",
    (
        (51.50183925568836, -0.14131817635799537, City.LONDON),
        (51.50183925568836, -0.14131817635799537, City.BERLIN),
        (51.50183925568836, -0.14131817635799537, City.NICOSIA),
    ),
)
async def test_get_city_by_coordinates(
    repository: CityRepository,
    some_city_latitude: float,
    some_city_longitude: float,
    expected_city: City,
):
    res = await repository.get_city_by_coordinates(latitude=some_city_latitude, longitude=some_city_longitude)

    assert res.name == expected_city
