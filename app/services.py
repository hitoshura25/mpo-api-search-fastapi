import httpx
import feedparser
from datetime import datetime
from typing import Dict, Any, List
from .models import Episode

def transform_podcast(podcast: Dict[str, Any]) -> Dict[str, Any]:
    field_mapping = {
        'name': ['trackName'],
        'artworkUrl': ['artworkUrl600', 'artworkUrl100'],
        'smallArtworkUrl': ['artworkUrl100'], 
        'genres': ['genres'],
        'author': ['artistName'],
        'feedUrl': ['feedUrl']
    }
    
    def get_first_value(fields: List[str]) -> Any:
        return next((podcast.get(field) for field in fields if podcast.get(field) is not None), None)
    
    return {
        new_key: get_first_value(possible_fields)
        for new_key, possible_fields in field_mapping.items()
    }

async def search_podcasts(term: str) -> Dict[str, Any]:
    params = {
        "term": term,
        "entity": "podcast"
    }

    with httpx.Client() as client:
        response = client.get(
            "https://itunes.apple.com/search",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "resultCount": data["resultCount"],
            "results": [transform_podcast(podcast) for podcast in data["results"]]
        }
    
async def get_podcast_episodes(feed_url: str, max_episodes: int = None) -> Dict[str, Any]:
    feed = feedparser.parse(feed_url) 
    image = feed.feed.get('image', {})
    episodes = []
    for entry in feed.entries:
        if max_episodes and len(episodes) >= max_episodes:
            break

        link = next(iter(entry.get('links', [])), {})
        episode = Episode(
            name=entry.get('title', ''),
            description=entry.get('description', ''),
            published=datetime.strptime(entry.get('published', ''), '%a, %d %b %Y %H:%M:%S %z'),
            length=entry.get('itunes_duration', ''),
            downloadUrl=link.get('href', ''),
            type=link.get('type', ''),
            artworkUrl=''
        )
        episodes.append(episode)
    
    return {
        "feed_url": feed_url,
        "episodes": episodes,
        "name": feed.feed.get('title', ''),
        "description": feed.feed.get('description', ''),
        "imageUrl": image.get('href', ''),
    }