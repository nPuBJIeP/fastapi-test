from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "balance": 60.0
    }

