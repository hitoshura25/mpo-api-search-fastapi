import httpx
from typing import Dict, Any, List

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