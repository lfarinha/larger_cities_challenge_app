import os

import pandas
from geopy.distance import geodesic

from larger_cities.exceptions.custom_exceptions import (
    NoDataInTSVFile,
    NoCitiesFoundForName,
)
from larger_cities.models.response_models import (
    NearbyCity,
    NearbyCityWithDistance,
    SuggestionsResponse,
)

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(os.getcwd()))


async def suggest_larger_cities(
    q: str,
    latitude: str | None = None,
    longitude: str | None = None,
) -> SuggestionsResponse:
    """
        Suggest larger cities to the user based on a partial or complete term

    Params:
        q (str): The partial (or complete) search term is passed as a query string parameter
        latitude (str): The latitude of the larger city to search for
        longitude (str): The longitude of the larger city to search for

    Returns:
        list (SuggestionRequest | None): Either return a list of results or an empty list

    Raises:


    """
    response: list[NearbyCity | None]
    cities: pandas.DataFrame = await get_cities_from_file()
    cities_by_name: pandas.DataFrame = await find_nearby_cities_by_name(cities, q)
    nearby_cities: list[NearbyCity] | list = await filter_nearby_cities_by_name(cities_by_name)

    if nearby_cities:
        if latitude and longitude:
            nearby_cities = await rank_nearby_cities_with_lat_and_log_provided(
                nearby_cities, latitude, longitude
            )
        nearby_cities = await rank_nearby_cities_without_lat_and_log_provided(
            nearby_cities, q
        )

    return SuggestionsResponse(suggestions=nearby_cities)


async def get_cities_from_file() -> pandas.DataFrame:
    """
    Read cities from a tsv file

    Returns:
        cities (pands.Dataframe): A dataframe with all the cities in the file.

    Raises:
        NoDataInTSVFile: if the file is empty.

    """
    cities: pandas.DataFrame = pandas.read_csv(
        f"{PROJECT_ROOT_DIR}/cities_canada-usa.tsv", delimiter="\t"
    )

    if cities.empty:
        raise NoDataInTSVFile("The TSV file may be empty.")

    return cities


async def find_nearby_cities_by_name(
    cities: pandas.DataFrame, q: str
) -> pandas.DataFrame:
    """
    Find all cities close to the input city

    Returns:
        cities (pandas.DataFrame): A dataframe with the near cities.

    """
    return cities[
        (cities["name"].str.lower().str.contains(q.lower()))
        & (cities["population"] > 5000)
    ]


async def filter_nearby_cities_by_name(
    cities_by_name: pandas.DataFrame,
) -> list[NearbyCity] | list:
    """
        Filter found nearby cities by name

    Params:
        cities_by_name (pandas.DataFrame): The cities to filter.

    Return:
        nearby_cities (list[NearbyCity]): The filtered result of the search or an empty list if no cities found.

    """
    nearby_cities: list[NearbyCity] = []

    if not cities_by_name.empty:
        nearby_cities = [
            NearbyCity(
                name=f'{city["name"]}, {city["admin1"]}, {city["country"]}',
                latitude=str(city["lat"]),
                longitude=str(city["long"]),
            )
            for city in cities_by_name.to_dict(orient="records")
        ]

    return nearby_cities


async def rank_nearby_cities_without_lat_and_log_provided(
    nearby_cities: list[NearbyCity],
    q: str,
) -> list[NearbyCity]:
    """
        Try to get a rough approximate of the score on how a city is relevant against user input
        when the user does not provide a latitude and longitude

    Params:
        nearby_cities (list[NearbyCities]): The list of nearby cities filtered from the dataset.
        q (str): The partial (or complete) search term is passed as a query string parameter
        latitude (str): The latitude of the larger city to search for
        longitude (str): The longitude of the larger city to search for

    Returns:
        nearby_cities (list[NearbyCities]): The list of nearby cities with a score 0 to 1 based on closeness to input city.

    """
    # Using Jaccard similarity index to count the number of common characters between two strings
    # more info on the approach https://en.wikipedia.org/wiki/Jaccard_index
    # approach taken from here https://www.learndatasci.com/glossary/jaccard-similarity/
    # first time using this approach :)
    for city in nearby_cities:
        nearby_city = set(city.name.lower())
        input_city = set(q.lower())
        intersection = len(input_city.intersection(nearby_city))
        union = len(input_city.union(nearby_city))
        city.score = round(intersection / union if union != 0 else 0, 1)

    # sort the nearby cities based on their rating score
    nearby_cities = sorted(nearby_cities, key=lambda x: x.score, reverse=True)

    return nearby_cities


async def rank_nearby_cities_with_lat_and_log_provided(
    nearby_cities: list[NearbyCity],
    latitude: str,
    longitude: str,
) -> list[NearbyCity]:
    """
        Try to get a rough approximate of the score on how a city is relevant against user input
        when the user provides a latitude and longitude

    Params:
        nearby_cities (list[NearbyCities]): The list of nearby cities filtered from the dataset.
        latitude (str): The latitude of the larger city to search for
        longitude (str): The longitude of the larger city to search for

    Returns:
        nearby_cities (list[NearbyCities]): The list of nearby cities with a score 0 to 1 based on closeness to input city.

    """
    nearby_cities_with_distance = []
    for nearby_city in nearby_cities:
        input_city_coordinates = (latitude, longitude)
        nearby_city_coordinates = (nearby_city.latitude, nearby_city.longitude)
        nearby_cities_with_distance.append(
            NearbyCityWithDistance(
                **nearby_city.model_dump(),
                distance=round(
                    geodesic(input_city_coordinates, nearby_city_coordinates).miles
                ),
            )
        )

    max_distance = max([city.distance for city in nearby_cities_with_distance])

    if not max_distance:
        # if no nearby cities were found just return an empty list
        return []

    nearby_cities = [
        NearbyCity(
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude,
            score=(
                round(1 - (city.distance / max_distance), 1)
            ),
        )
        for city in nearby_cities_with_distance
    ]

    # sort the nearby cities based on their rating score
    nearby_cities = sorted(nearby_cities, key=lambda x: x.score, reverse=True)

    return nearby_cities
