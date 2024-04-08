import pytest
from fastapi.testclient import TestClient
from starlette import status

from larger_cities.app import app
from larger_cities.models.response_models import NearbyCity, SuggestionsResponse


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, status_code",
    [
        ("London", status.HTTP_200_OK),
        ("Ajax", status.HTTP_200_OK),
        ("Bay Roberts", status.HTTP_200_OK),
        ("Bécancour", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("Côte-Saint-Luc", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("Baie-Comeau", status.HTTP_200_OK),
        ("Bois-des-Filion", status.HTTP_200_OK),
        ("Bradford West Gwillimbury", status.HTTP_200_OK),
    ],
)
async def test_verify_only_valid_characters_are_allowed_in_q(client, q, status_code):
    response = client.get(f"/suggestions", params={"q": q})

    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        nearby_cities: list[NearbyCity] = [
            NearbyCity(**city)
            for city in SuggestionsResponse(**response.json()).suggestions
        ]

        for nearby_city in nearby_cities:
            assert nearby_city.name
            assert nearby_city.latitude
            assert nearby_city.longitude
            assert nearby_city.score >= 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, latitude, longitude, status_code",
    [
        ("London", "42.98339", "-81.23304", status.HTTP_200_OK),
        ("Ajax", "43.85012", "-79.03288", status.HTTP_200_OK),
        ("Aylmer", "42.76679", "-80.98302", status.HTTP_200_OK),
    ],
)
async def test_verify_only_valid_characters_are_allowed_in_latitude_longitude(
    client, q, latitude, longitude, status_code
):
    response = client.get(
        f"/suggestions", params={"q": q, "latitude": latitude, "longitude": longitude}
    )

    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        nearby_cities: list[NearbyCity] = [
            NearbyCity(**city)
            for city in SuggestionsResponse(**response.json()).suggestions
        ]

        for nearby_city in nearby_cities:
            assert nearby_city.name
            assert nearby_city.latitude
            assert nearby_city.longitude
            assert nearby_city.score >= 0
