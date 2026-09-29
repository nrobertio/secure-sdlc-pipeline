from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    assert client.get("/").status_code == 200


def test_healthz():
    assert client.get("/healthz").json()["status"] == "healthy"
