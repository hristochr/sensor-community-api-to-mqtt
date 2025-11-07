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
    """Verify HTTP Basic Authentication credentials"""
    # Ensure variables are str
    username = str(credentials.username)
    password = str(credentials.password)
    api_user = str(API_USERNAME)
    api_pass = str(API_PASSWORD)

    is_username_correct = secrets.compare_digest(username, api_user)
    is_password_correct = secrets.compare_digest(password, api_pass)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return username
