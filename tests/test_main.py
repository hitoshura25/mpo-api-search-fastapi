import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import search_podcasts
from unittest.mock import patch, MagicMock
from pytest_httpx import HTTPXMock

client = TestClient(app)

def load_json_fixture(filename):
    fixtures_dir = Path(__file__).parent / "fixtures"
    file_path = fixtures_dir / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def create_mock_feed():
    mock_feed = MagicMock()
    mock_feed.feed = {
        'title': 'Game Scoop!',
        'description': 'Veteran games industry host Daemon Hatfield and the IGN crew break down the biggest gaming news of the week, dive into retro gaming nostalgia, and challenge each other—and the audience—with trivia that puts even hardcore gamers to the test.',
        'image': {'href': 'https://megaphone.imgix.net/podcasts/6c7d19b0-729e-11ee-ab31-cb7b4e09a1f7/image/49bfd96ed9d8a8f3d7ee2a344fe303f0.jpg?ixlib=rails-4.3.1&max-w=3000&max-h=3000&fit=crop&auto=format,compress'}
    }
    mock_feed.entries = [{
        'title': 'Game Scoop! 813: The Witcher 3 & Cyberpunk Hit Important Milestones',
        'description': 'Welcome back to IGN Game Scoop!, the ONLY video game podcast! This week your Omega Cops -- Daemon Hatfield, Sam Claiborn, and Justin Davis -- are discussing The Witcher 3, Cyberpunk 2, Black Panther, The Last of Us, and more.',
        'published': 'Fri, 30 May 2025 20:24:00 -0000',
        'itunes_duration': '4336',
        'links': [{'href': 'https://www.podtrac.com/pts/redirect.mp3/pdst.fm/e/chrt.fm/track/FGADCC/pscrb.fm/rss/p/tracking.swap.fm/track/bwUd3PHC9DH3VTlBXDTt/traffic.megaphone.fm/SBP4198775748.mp3?updated=1748636657', 'type': 'audio/mpeg'}]
    }]
    return mock_feed

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_search_podcast_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://itunes.apple.com/search?term=python&entity=podcast",
        method="GET",
        json=load_json_fixture("itunes_search_response.json")
    )

    response = client.get("/search?term=python")
    assert response.status_code == 200
    assert response.json() == load_json_fixture("expected_search_response.json")

def test_search_podcast_empty_term():
    response = client.get("/search/?term=")
    assert response.status_code == 422

def test_search_podcast_service_error():
    with patch('app.main.search_podcasts') as mock_search:
        mock_search.side_effect = Exception("Service error")
        response = client.get("/search/?term=python")
        
        assert response.status_code == 500
        assert "Service error" in response.json()["detail"]

def test_podcast_details_success(monkeypatch):
    mock_feed = create_mock_feed()
    monkeypatch.setattr('feedparser.parse', lambda _: mock_feed)
    response = client.get("/details?feed_url=https%3A%2F%2Ffeeds.megaphone.fm%2Fgamescoop&max_episodes=1")
    assert response.status_code == 200
    assert response.json() == load_json_fixture("expected_details_response.json")

