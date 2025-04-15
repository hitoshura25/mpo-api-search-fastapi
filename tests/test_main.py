import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import search_podcasts
from unittest.mock import patch
from pytest_httpx import HTTPXMock

client = TestClient(app)

def load_json_fixture(filename):
    fixtures_dir = Path(__file__).parent / "fixtures"
    file_path = fixtures_dir / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

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
