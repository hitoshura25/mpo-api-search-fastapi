from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

class Episode(BaseModel):
    name: str
    description: Optional[str] = None
    published: Optional[datetime] = None
    length: Optional[str] = None
    downloadUrl: Optional[str] = None
    type: Optional[str] = None
    artworkUrl: Optional[str] = None

class EpisodeResponse(BaseModel):
    name: str
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    episodes: List[Episode]