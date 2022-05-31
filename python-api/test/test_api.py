import os
from base64 import b64encode

import main
from fastapi.testclient import TestClient


def encode_basic_auth(username, password):
    return "Basic " + b64encode(str.encode(f"{username}:{password}")).decode("ascii")


client = TestClient(main.app)
ADMIN_USERNAME = os.environ["LEDN_ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["LEDN_ADMIN_PASSWORD"]
AUTH_HEADER = encode_basic_auth(ADMIN_USERNAME, ADMIN_PASSWORD)
BAD_PASSWORD_AUTH_HEADER = encode_basic_auth(ADMIN_USERNAME, "Bad password")


def test_get_account():
    response = client.get(
        "/accounts/Cassandre10@gmail.com", headers={"Authorization": AUTH_HEADER}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "Cassandre10@gmail.com"
    assert response.json()["firstName"] == "Sydnie"


def test_get_account_bad_password():
    response = client.get(
        "/accounts/Cassandre10@gmail.com",
        headers={"Authorization": BAD_PASSWORD_AUTH_HEADER},
    )
    assert response.status_code == 401


def test_get_account_no_auth():
    response = client.get(
        "/accounts/Cassandre10@gmail.com",
    )
    assert response.status_code == 401


def test_get_account_bad_email():
    response = client.get(
        "/accounts/notfound@gmail.com", headers={"Authorization": AUTH_HEADER}
    )
    assert response.status_code == 404


def test_get_account_balance_bad_email():
    response = client.get("/accounts/notfound@gmail.com/balance")
    # Arguably, this should return a 404, but still seems like it would be a valid response
    assert response.json() == 0


def test_create_transaction():
    response = client.post(
        "/transactions",
        json={
            "userEmail": "testuser@test.com",
            "amount": 5,
            "type": "receive",
            "createdAt": "2019-12-20T20:18:11.806Z",
        },
    )
    assert response.status_code == 201


def test_create_transfer():
    response = client.post(
        "/transfers",
        json={
            "fromEmail": "from@email.com",
            "toEmail": "to@email.com",
            "amount": 10,
            "createdAt": "2019-12-20T20:18:11.806Z",
        },
    )
    assert response.status_code == 201
    assert len(response.json()) == 2
