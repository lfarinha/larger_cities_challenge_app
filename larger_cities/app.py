import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from larger_cities.tools.logger import setup_logger

from larger_cities.exceptions.custom_exceptions import NoDataInTSVFile
from larger_cities.models.response_models import SuggestionsResponse
from larger_cities.tools.manage_suggestions import suggest_larger_cities


logger = setup_logger(__name__)

app = FastAPI(title="Suggestions API Challenge")

# Update origins appropriately before moving to PROD
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home() -> str:
    return "Home is where your heart is..."


@app.get("/suggestions", response_model=SuggestionsResponse)
async def suggestions(
    q: str = Query(pattern="^[a-zA-Z -]+$"),
    latitude: str = Query(default=None, pattern=r"^-?\d+(\.\d+)?$"),
    longitude: str = Query(default=None, pattern=r"^-?\d+(\.\d+)?$"),
) -> SuggestionsResponse | HTTPException:
    """
    Endpoint to handle requests for suggestions from the users.

    Params:
        q: (str): The partial (or complete) search term is passed as a query string parameter
        latitude (str): The latitude of the larger city to search for
        longitude (str): The longitude of the larger city to search for

    Returns:
        response (list[SuggestionResponse | None]): Either the list of larger cities or an empty list

    Raises:
        NoDataInTSVFile: if no data is found in the tsv file
        HTTPException: if there is an internal error that prevents the processing of the request

    """
    response: SuggestionsResponse | None = None
    try:
        response = await suggest_larger_cities(q, latitude, longitude)
    except NoDataInTSVFile as e:
        logger.debug(f"Error: {e}")
        return HTTPException(
            status_code=500,
            detail="Could not read from data file. Please try again later.",
        )
    except Exception as e:
        logger.debug(f"Error: {e}")
        return HTTPException(
            status_code=500,
            detail=str(e),
        )
    finally:
        return response


if __name__ == "__main__":
    uvicorn.run(app=app, port=5000, host="0.0.0.0", log_level="info")
