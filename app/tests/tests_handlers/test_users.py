import json

from app.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


@pytest.fixture
def user_id():
    return -1


@pytest.fixture()
def create_user_request(user_id):
    return {
        "user_id": user_id,
        "balance": 0
    }


def test_get_user_not_exists(user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_create_user(user_id, create_user_request):
    response = client.post("/users", content=json.dumps(create_user_request))
    assert response.status_code == 200
    assert response.json() == create_user_request


def test_get_user(user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": user_id,
        "balance": 0
    }


def test_withdraw_balance_insufficient_funds():
    before_user_response = client.get("/users/1")
    assert before_user_response.status_code == 200
    withdraw_response = client.post("/balance/withdraw", content=json.dumps({"user_id": 1, "amount": 5}))
    assert withdraw_response.status_code == 400
    assert withdraw_response.json() == {"detail": "Insufficient funds"}


def test_delete_user(user_id):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
