from pydantic import BaseModel, Field


class NearbyCity(BaseModel):
    """
    NearbyCities response model
    """

    name: str = Field(description="The name of the city including state and country")
    latitude: str = Field(description="The latitude of the city")
    longitude: str = Field(description="The longitude of the city")
    score: float | None = Field(
        default=None, description="The confidence in the suggestion"
    )


class NearbyCityWithDistance(BaseModel):
    """
    NearbyCities with Distance response model
    """

    name: str = Field(description="The name of the city including state and country")
    latitude: str = Field(description="The latitude of the city")
    longitude: str = Field(description="The longitude of the city")
    score: float | None = Field(
        default=None, description="The confidence in the suggestion"
    )
    distance: int = Field(
        description="The distance between the input city and the closest city"
    )


class SuggestionsResponse(BaseModel):
    suggestions: list[NearbyCity] | list = Field(
        description="The result of the search of the largest closest city"
    )
