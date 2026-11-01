import os

os.environ["MOCK_MODE"] = "true"

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_blog_mock():
    response = client.post(
        "/api/blog/generate",
        json={
            "topic": "Agentic AI",
            "audience": "AI engineers",
            "tone": "professional",
            "target_words": 800,
            "keywords": ["agentic AI"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["topic"] == "Agentic AI"
    assert body["mode"] == "mock"
    assert body["final_blog"]
