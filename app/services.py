import httpx
import feedparser
from time import mktime
from datetime import datetime
from typing import Dict, Any, List, Optional
from .models import Episode


def parse_duration(duration_str: str) -> Optional[str]:
    if not duration_str:
        return None
        
    # Handle HH:MM:SS format
    if ':' in duration_str:
        parts = duration_str.split(':')
        parts = [int(p) for p in parts]
        if len(parts) == 3:
            return str(parts[0] * 3600 + parts[1] * 60 + parts[2])
        elif len(parts) == 2:
            return str(parts[0] * 60 + parts[1])
            
    return duration_str

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
    
async def get_podcast_episodes(feed_url: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
    feed = feedparser.parse(feed_url) 
    total_episodes = len(feed.entries)
    image = feed.feed.get('image', {})
    paginated_entries = feed.entries[offset:offset + limit]
    episodes = []
    for entry in paginated_entries:
        link = next((link for link in entry.get('links', []) if link.get('rel') == 'enclosure'), {})
        media_thumbnail = next(iter(entry.get('media_thumbnail', [])), {})
        media_content = next(iter(entry.get('media_content', [])), {})
        entry_image = entry.get('image', {})
        length = parse_duration(media_content.get('duration') or entry.get('itunes_duration') or link.get('length', ''))
        episode = Episode(
            name=entry.get('title', ''),
            description=entry.get('description', ''),
            published=datetime.fromtimestamp(mktime(entry.get('published_parsed', ''))),
            durationInSeconds=length,
            downloadUrl=link.get('href', ''),
            type=link.get('type', ''),
            artworkUrl=media_thumbnail.get('url', entry_image.get('href', image.get('href', '') )),
        )
        episodes.append(episode)
    
    next_offset = offset + limit if offset + limit < total_episodes else None
    prev_offset = offset - limit if offset > 0 else None
    return {
        "feed_url": feed_url,
        "episodes": episodes,
        "name": feed.feed.get('title', ''),
        "description": feed.feed.get('description', ''),
        "imageUrl": image.get('href', ''),
        "pagination": {
            "total": total_episodes,
            "limit": limit,
            "offset": offset,
            "next_page": f"/details/?feed_url={feed_url}&limit={limit}&offset={next_offset}" if next_offset != None else None,
            "previous_page": f"/details/?feed_url={feed_url}&limit={limit}&offset={prev_offset}" if prev_offset != None else None
        }
    }