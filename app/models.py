from pydantic import BaseModel
from typing import List, Optional

class Podcast(BaseModel):
    name: Optional[str] = None
    artworkUrl: Optional[str] = None
    smallArtworkUrl: Optional[str] = None
    genres: Optional[List[str]] = None
    author: Optional[str] = None
    feedUrl: Optional[str] = None

class PodcastResponse(BaseModel):
    resultCount: int
    results: List[Podcast]