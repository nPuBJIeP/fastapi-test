from fastapi.testclient import TestClient

from app.main import app
import pytest

client = TestClient(app)


def test_read_main():
    response = client.get("/users/1")
    print(response)
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "balance": 60.0
    }

