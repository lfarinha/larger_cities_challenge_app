import uvicorn
from fastapi import FastAPI, HTTPException, Query

from larger_cities.models.request_models import SuggestionRequest
from larger_cities.models.response_models import SuggestionResponse
from larger_cities.tools.manage_suggestions import suggest_larger_cities

app = FastAPI()


@app.get("/")
async def home() -> str:
    return "Home is where your heart is..."


@app.get("/suggestions", response_model=SuggestionResponse)
async def suggestions(
    q: str = Query(),
    latitude: str = Query(default=None),
    longitude: str = Query(default=None),
) -> list[SuggestionResponse | None] | HTTPException:
    """
    Endpoint to handle requests for suggestions from the users.

    Params:
        q: (str): The partial (or complete) search term is passed as a query string parameter
        latitude (str): The latitude of the larger city to search for
        longitude (str): The longitude of the larger city to search for

    Returns:
        response (list[SuggestionResponse | None]): Either the list of larger cities or an empty list

    Raises:
        HTTPException: if there is an internal error that prevents the processing of the request

    """
    response: list[SuggestionResponse | None] = None
    try:
        response = await suggest_larger_cities(q, latitude, longitude)
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        if response:
            return response


if __name__ == "__main__":
    uvicorn.run(app=app, port=5000, host="0.0.0.0")
