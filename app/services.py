import httpx
from typing import Dict, Any

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
        return response.json()