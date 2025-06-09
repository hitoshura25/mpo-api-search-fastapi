from fastapi import FastAPI, HTTPException, Query
from .models import PodcastResponse, EpisodeResponse
from .services import search_podcasts, get_podcast_episodes

app = FastAPI(title="Podcast Search API")

@app.get("/search/", response_model=PodcastResponse, response_model_exclude_none=True)
async def search_podcast_endpoint(
    term: str = Query(..., min_length=1, description="Search term for podcasts")
):
    try:
        results = await search_podcasts(term)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/details/", response_model=EpisodeResponse, response_model_exclude_none=True)
async def get_podcast_details(
    feed_url: str = Query(..., description="RSS feed URL of the podcast"),
    episode_limit: int = Query(default=10, ge=1, description="Maximum number of episodes to return", include_in_schema=True),
    episode_offset: int = Query(default=0, ge=0, description="Offset position for episodes to return", include_in_schema=True)
):
    try:
        results = await get_podcast_episodes(feed_url, episode_limit, episode_offset)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}