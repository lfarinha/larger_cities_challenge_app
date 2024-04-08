import uvicorn
from fastapi import FastAPI, HTTPException

from larger_cities.models.request_models import SuggestionRequest
from larger_cities.models.response_models import SuggestionResponse

app = FastAPI()


@app.get("/suggestions", response_model=SuggestionResponse)
async def suggestions(request: SuggestionRequest) -> SuggestionResponse | HTTPException:
    response: SuggestionResponse | None = None
    try:

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
