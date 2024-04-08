from larger_cities.models.request_models import SuggestionRequest
from larger_cities.models.response_models import SuggestionResponse


async def suggest_larger_cities(request: SuggestionRequest) -> list[SuggestionRequest | None]:
    """
        Suggest larger cities to the user based on a partial or complete term

    Params:
        request (SuggestionRequest): The Suggestion request from the user.

    Returns:
        list (SuggestionRequest | None): Either return a list of results or an empty list

    Raises:


    """
    response: list[SuggestionRequest | None]
