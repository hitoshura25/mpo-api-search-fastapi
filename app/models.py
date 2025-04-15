from pydantic import BaseModel
from typing import List, Optional

class PodcastResult(BaseModel):
    trackId: Optional[int] = None
    trackName: Optional[str] = None
    artistName: Optional[str] = None
    description: Optional[str] = None
    primaryGenreName: Optional[str] = None
    releaseDate: Optional[str] = None
    feedUrl: Optional[str] = None
    artworkUrl600: Optional[str] = None

class PodcastResponse(BaseModel):
    resultCount: int
    results: List[PodcastResult]