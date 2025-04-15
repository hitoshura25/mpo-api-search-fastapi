from fastapi import FastAPI, HTTPException, Query
from .models import PodcastResponse
from .services import search_podcasts

app = FastAPI(title="Podcast Search API")

@app.get("/search/", response_model=PodcastResponse)
async def search_podcast_endpoint(
    term: str = Query(..., min_length=1, description="Search term for podcasts")
):
    try:
        results = await search_podcasts(term)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}