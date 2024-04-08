from pydantic import BaseModel, Field


class SuggestionRequest(BaseModel):
    """Suggestion request model"""

    q: str = Field(
        description="The partial (or complete) search term is passed as a query string parameter"
    )
    latitude: str | None = Field(
        default=None, description="The latitude of the larger city to search for"
    )
    longitude: str | None = Field(
        default=None, description="The longitude of the larger city to search for"
    )
