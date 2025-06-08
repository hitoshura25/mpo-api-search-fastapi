import json
from pathlib import Path
import time
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from pytest_httpx import HTTPXMock

client = TestClient(app)

def load_json_fixture(filename):
    fixtures_dir = Path(__file__).parent / "fixtures"
    file_path = fixtures_dir / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def create_mock_feed():
    format_string = "%Y-%m-%d %H:%M:%S"
    mock_feed = MagicMock()
    mock_feed.feed = {
        'title': 'Test Podcast',
        'description': 'Test Description',
        'image': {'href': 'https://example.com/default.jpg'}
    }
    mock_feed.entries = [
        {
            'title': 'Complete Episode',
            'description': 'Full description',
            'published_parsed': time.strptime('2025-06-08 15:30:00', format_string),
            'itunes_duration': '01:30:45',
            'links': [
                {'href': 'https://example.com/episode1.mp3', 'rel': 'enclosure', 'type': 'audio/mpeg'},
                {'href': 'https://example.com/episode1', 'rel': 'alternate'}
            ],
            'image': {'href': 'https://example.com/ep1.jpg'},
            'media_thumbnail': [{'url': 'https://example.com/thumb1.jpg'}]
        },
        {
            'title': 'Minimal Episode',
            'description': None,
            'published_parsed': time.strptime('2025-03-22 01:02:00', format_string),
            'links': [{'href': 'https://example.com/episode2.mp3', 'rel': 'enclosure'}]
        },
        {
            'title': 'Duration in Seconds',
            'description': 'Test description',
            'published_parsed': time.strptime('2025-05-29 15:00:00', format_string),
            'itunes_duration': '3600',
            'links': [{'href': 'https://example.com/episode3.mp3', 'rel': 'enclosure'}],
            'media_content': [{'duration': '3600'}]
        },
        {
            'title': 'Multiple Artwork Sources',
            'description': 'Test description',
            'published_parsed': time.strptime('2025-05-28 10:00:00', format_string),
            'itunes_duration': '45:30',
            'links': [{'href': 'https://example.com/episode4.mp3', 'rel': 'enclosure'}],
            'image': {'href': 'https://example.com/ep4.jpg'},
            'media_thumbnail': [{'url': 'https://example.com/thumb4.jpg'}],
            'media_content': [{'url': 'https://example.com/content4.jpg'}]
        }
    ]
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

def test_podcast_details_with_offset_and_limit_success(monkeypatch):
    mock_feed = create_mock_feed()
    monkeypatch.setattr('feedparser.parse', lambda _: mock_feed)
    response = client.get("/details?feed_url=https://rss.pdrl.fm/817ebc/feeds.megaphone.fm/gamescoop&offset=1&limit=1")
    assert response.status_code == 200
    assert response.json() == load_json_fixture("expected_details_with_offset_and_limit_response.json")

