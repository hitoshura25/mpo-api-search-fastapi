from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict()

class Podcast(BaseModelWithConfig):
    name: Optional[str] = None
    artworkUrl: Optional[str] = None
    smallArtworkUrl: Optional[str] = None
    genres: Optional[List[str]] = None
    author: Optional[str] = None
    feedUrl: Optional[str] = None

class PodcastResponse(BaseModelWithConfig):
    resultCount: int
    results: List[Podcast]

class Episode(BaseModelWithConfig):
    name: str
    description: Optional[str] = None
    published: Optional[datetime] = None
    durationInSeconds: Optional[str] = None
    downloadUrl: Optional[str] = None
    type: Optional[str] = None
    artworkUrl: Optional[str] = None

class PaginationMetadata(BaseModelWithConfig):
    total: int
    limit: int
    offset: int
    next_page: Optional[str] = None
    previous_page: Optional[str] = None

class EpisodeResponse(BaseModelWithConfig):
    name: str
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    episodes: List[Episode]
    pagination: PaginationMetadata