import os
import secrets

from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

http_basic = HTTPBasic()

ADMIN_USERNAME = os.environ["LEDN_ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["LEDN_ADMIN_PASSWORD"]


def validate_credentials(credentials: HTTPBasicCredentials):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
