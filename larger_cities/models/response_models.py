from pydantic import BaseModel, Field


class NearbyCities(BaseModel):
    """
    Suggestions response model
    """

    name: str = Field(description="The name of the city including state and country")
    latitude: str = Field(description="The latitude of the city")
    longitude: str = Field(description="The longitude of the city")
    score: float | None = Field(
        default=None, description="The confidence in the suggestion"
    )
