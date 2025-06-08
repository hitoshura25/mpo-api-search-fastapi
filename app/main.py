from fastapi import FastAPI, HTTPException, Query
from .models import PodcastResponse, EpisodeResponse
from .services import search_podcasts, get_podcast_episodes

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
    
@app.get("/details/", response_model=EpisodeResponse)
async def get_podcast_details(
    feed_url: str = Query(..., description="RSS feed URL of the podcast"),
    max_episodes: int = Query(default=None, ge=1, description="Maximum number of episodes to return", include_in_schema=True)
):
    try:
        results = await get_podcast_episodes(feed_url, max_episodes)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}