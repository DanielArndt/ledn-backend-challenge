from fastapi import FastAPI
from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def test_get_account():
    response = client.get("/accounts/Cassandre10@gmail.com")
    assert response.status_code == 200
    assert response.json()["email"] == "Cassandre10@gmail.com"
    assert response.json()["firstName"] == "Sydnie"


def test_get_account_bad_email():
    response = client.get("/accounts/notfound@gmail.com")
    assert response.status_code == 404
