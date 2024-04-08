import pandas

from larger_cities.models.response_models import NearbyCities


async def suggest_larger_cities(
    q: str,
    latitude: str = None,
    longitude: str = None,
) -> list[NearbyCities | None]:
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
    response: list[NearbyCities | None]
    cities: pandas.DataFrame = pandas.read_csv("cities_canada-usa.tsv", delimiter="\t")
    cities_by_name: pandas.DataFrame = cities[cities["name"].str.contains(q)]

    if not cities_by_name.empty:
        nearby_cities = [
            NearbyCities(
                name=f'{city["name"]}, {city["country"]}',
                latitude=str(city["lat"]),
                longitude=str(city["long"]),
            )
            for city in cities_by_name[cities_by_name["name"]].to_dict(orient="records")
        ]

    else:
        cities_by_alt_name: pandas.DataFrame = cities["alt_name"].to_list()
        if q in cities_by_alt_name:
            nearby_cities = [
                NearbyCities(
                    name=f'{city["name"]}, {city["country"]}',
                    latitude=str(city["lat"]),
                    longitude=str(city["long"]),
                )
                for city in cities_by_alt_name[cities_by_alt_name["alt_name"]].to_dict(
                    orient="records"
                )
            ]

    if not latitude and not longitude:
        scored_cities = await rank_nearby_cities_without_lat_and_log_provided(
            nearby_cities, q
        )

    return scored_cities


async def rank_nearby_cities_without_lat_and_log_provided(
    nearby_cities: list[NearbyCities],
    q: str,
) -> list[NearbyCities]:
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

    return nearby_cities


async def rank_nearby_cities_with_lat_and_log_provided(
    nearby_cities: list[NearbyCities],
    q: str,
    latitude: str,
    longitude: str,
) -> list[NearbyCities]:
    """
        Try to get a rough approximate of the score on how a city is relevant against user input
        when the user provides a latitude and longitude

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

    return nearby_cities
