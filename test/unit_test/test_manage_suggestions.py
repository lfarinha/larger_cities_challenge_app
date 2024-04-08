import pandas
import pytest

from larger_cities.models.response_models import NearbyCity
from larger_cities.tools.manage_suggestions import (
    suggest_larger_cities,
    rank_nearby_cities_with_lat_and_log_provided,
    find_nearby_cities_by_name,
    get_cities_from_file,
    filter_nearby_cities_by_name,
    rank_nearby_cities_without_lat_and_log_provided,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, latitude, longitude",
    [
        ("London", None, None),
        ("London", "43.70011", "-79.4163"),
        ("Londonasd", "43.70011", "-79.4163"),
    ],
)
async def test_suggestion_requests(q, latitude, longitude):
    """Verify the list of nearby cities is returning valid values"""

    result = await suggest_larger_cities(q, latitude, longitude)

    for city in result.suggestions:
        assert city.name
        assert q in city.name
        assert city.latitude
        assert city.longitude
        assert city.score >= 0


@pytest.mark.parametrize(
    "q, latitude, longitude, expected",
    [
        (
            "Ajax",
            "43.85012",
            "-79.03288",
            [],
        ),
        (
            "London",
            "43.70011",
            "-79.4163",
            [
                NearbyCity(
                    name="London, 08, CA",
                    latitude="42.98339",
                    longitude="-81.23304",
                    score=0.8,
                ),
                NearbyCity(
                    name="Londontowne, MD, US",
                    latitude="38.93345",
                    longitude="-76.54941",
                    score=0.3,
                ),
                NearbyCity(
                    name="London, OH, US",
                    latitude="39.88645",
                    longitude="-83.44825",
                    score=0.3,
                ),
                NearbyCity(
                    name="New London, WI, US",
                    latitude="44.39276",
                    longitude="-88.73983",
                    score=0.1,
                ),
                NearbyCity(
                    name="London, KY, US",
                    latitude="37.12898",
                    longitude="-84.08326",
                    score=0.0,
                ),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_rank_nearby_cities_with_lat_and_log_provided(
    q, latitude, longitude, expected
):
    """Verify the rank with latitude and longitude provides results"""
    cities = await get_cities_from_file()
    nearby_cities = await find_nearby_cities_by_name(cities, q)
    nearby_cities_list = await filter_nearby_cities_by_name(nearby_cities)
    rank_cities = await rank_nearby_cities_with_lat_and_log_provided(
        nearby_cities_list, latitude, longitude
    )
    assert rank_cities == expected


@pytest.mark.parametrize(
    "q, expected",
    [
        (
            "Ajax",
            [
                NearbyCity(
                    name="Ajax, 08, CA",
                    latitude="43.85012",
                    longitude="-79.03288",
                    score=0.4,
                )
            ],
        ),
        (
            "London",
            [
                NearbyCity(
                    name="London, 08, CA",
                    latitude="42.98339",
                    longitude="-81.23304",
                    score=0.4,
                ),
                NearbyCity(
                    name="London, KY, US",
                    latitude="37.12898",
                    longitude="-84.08326",
                    score=0.4,
                ),
                NearbyCity(
                    name="London, OH, US",
                    latitude="39.88645",
                    longitude="-83.44825",
                    score=0.4,
                ),
                NearbyCity(
                    name="New London, WI, US",
                    latitude="44.39276",
                    longitude="-88.73983",
                    score=0.4,
                ),
                NearbyCity(
                    name="Londontowne, MD, US",
                    latitude="38.93345",
                    longitude="-76.54941",
                    score=0.3,
                ),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_rank_nearby_cities_without_lat_and_log_provided(q, expected):
    """Verify the nearby cities are returning valid scoring"""
    cities = await get_cities_from_file()
    nearby_cities = await find_nearby_cities_by_name(cities, q)
    nearby_cities_list = await filter_nearby_cities_by_name(nearby_cities)
    rank_cities = await rank_nearby_cities_without_lat_and_log_provided(
        nearby_cities_list,
        q,
    )
    assert rank_cities == expected
