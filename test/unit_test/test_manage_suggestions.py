import pandas
import pytest

from larger_cities.tools.manage_suggestions import suggest_larger_cities


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q, latitude, longitude, expected",
    [
        # ("London", None, None, ""),
        ("Londonas", None, None, ""),
        # ("London", "43.70011", "-79.4163", ""),
    ],
)
async def test_suggestion_requests(q, latitude, longitude, expected):
    """Verify the list of nearby cities is returning valid values"""

    suggestions = await suggest_larger_cities(q, latitude, longitude)
    print(suggestions)

    assert suggestions

    for city in suggestions:
        assert city.name
        assert q in city.name
        assert city.latitude
        assert city.longitude
        assert city.score
