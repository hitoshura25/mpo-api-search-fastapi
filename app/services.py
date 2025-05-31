import httpx
from typing import Dict, Any

def transform_podcast(podcast: Dict[str, Any]) -> Dict[str, Any]:
    field_mapping = {
        'trackName': 'name',
        'artworkUrl600': 'artworkUrl',
        'artworkUrl100': 'smallArtworkUrl', 
        'genres': 'genres',
        'artistName': 'author',
        'feedUrl': 'feedUrl'
    }
    
    return {
        new_key: podcast.get(old_key) 
        for old_key, new_key in field_mapping.items()
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