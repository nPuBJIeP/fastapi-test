import json

from app.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


@pytest.fixture
def sender_id():
    return -1


@pytest.fixture
def recipient_id():
    return -2


@pytest.fixture
def start_balance():
    return 10


@pytest.fixture
def increased_balance():
    return 30


@pytest.fixture
def increasing_amount():
    return 20


@pytest.fixture()
def create_first_user_request(sender_id, start_balance):
    return {
        "user_id": sender_id,
        "balance": start_balance
    }


@pytest.fixture()
def create_second_user_request(recipient_id, start_balance):
    return {
        "user_id": recipient_id,
        "balance": start_balance
    }


def test_get_user_not_exists(sender_id):
    response = client.get(f"/users/{sender_id}")
    assert response.status_code == 404


def test_create_user(sender_id, create_first_user_request):
    response = client.post("/users", content=json.dumps(create_first_user_request))
    assert response.status_code == 200
    assert response.json() == create_first_user_request


def test_get_user(sender_id, create_first_user_request):
    response = client.get(f"/users/{sender_id}")
    assert response.status_code == 200
    assert response.json() == create_first_user_request


def test_add_balance(sender_id, increasing_amount, increased_balance):
    before_user_response = client.get(f"/users/{sender_id}")
    assert before_user_response.status_code == 200
    withdraw_response = client.post("/balance/add",
                                    content=json.dumps({"user_id": sender_id, "amount": increasing_amount}))
    assert withdraw_response.status_code == 200
    assert withdraw_response.json() == {
        "user_id": sender_id,
        "balance": increased_balance
    }


def test_withdraw_balance(sender_id, start_balance):
    before_user_response = client.get(f"/users/{sender_id}")
    assert before_user_response.status_code == 200
    withdraw_response = client.post("/balance/withdraw", content=json.dumps({"user_id": sender_id, "amount": 20}))
    assert withdraw_response.status_code == 200
    assert withdraw_response.json() == {
        "user_id": sender_id,
        "balance": start_balance
    }


def test_transfer_balance(sender_id, recipient_id, create_second_user_request):
    second_user_response = client.post("/users", content=json.dumps(create_second_user_request))

    assert second_user_response.status_code == 200
    assert second_user_response.json() == create_second_user_request

    withdraw_response = client.post("/balance/transfer", content=json.dumps({
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "amount": 5
    }))
    assert withdraw_response.status_code == 200
    assert withdraw_response.json() == {
        "sender": {
            "user_id": sender_id,
            "balance": 5.0
        },
        "recipient": {
            "user_id": recipient_id,
            "balance": 15.0
        }
    }


def test_withdraw_balance_insufficient_funds(sender_id):
    before_user_response = client.get(f"/users/{sender_id}")
    assert before_user_response.status_code == 200
    withdraw_response = client.post("/balance/withdraw", content=json.dumps({"user_id": sender_id, "amount": 20}))
    assert withdraw_response.status_code == 400
    assert withdraw_response.json() == {"detail": "Insufficient funds"}


def test_delete_first_user(sender_id):
    response = client.delete(f"/users/{sender_id}")
    assert response.status_code == 200


def test_delete_second_user(recipient_id):
    response = client.delete(f"/users/{recipient_id}")
    assert response.status_code == 200
