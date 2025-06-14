import os
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


load_dotenv()

security = HTTPBasic()

API_USERNAME = os.getenv("API_USERNAME", '')
API_PASSWORD = os.getenv("API_PASSWORD", '')


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify the HTTP Basic Authentication credentials"""
    is_username_correct = secrets.compare_digest(credentials.username, API_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, API_PASSWORD)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
