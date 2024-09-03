import json

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    # assert response.json() == {
    #     "user_id": 1,
    #     "balance": 80.0
    # }


def test_withdraw_balance():
    before_user_response = client.get("/users/1")
    assert before_user_response.status_code == 200
    withdraw_response = client.post("/balance/withdraw", content=json.dumps({"user_id": 1, "amount": 5}))
    assert withdraw_response.status_code == 200
    assert withdraw_response.json() == {"user_id": 1, "balance": before_user_response.json()['balance'] - 5}
