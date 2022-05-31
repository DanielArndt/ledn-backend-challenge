import main
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient

client = TestClient(main.app)


def test_150k_records():
    response = client.get("/accounts/testuser@test.com/balance")
    initial_balance = response.json()
    for _ in range(150_000):
        response = client.post(
            "/transactions",
            json={
                "userEmail": "testuser@test.com",
                "amount": 5,
                "type": "credit",
                "createdAt": "2019-12-20T20:18:11.806Z",
            },
        )
    response = client.get("/accounts/testuser@test.com/balance")
    assert response.json() == initial_balance + (5 * 150_000)
