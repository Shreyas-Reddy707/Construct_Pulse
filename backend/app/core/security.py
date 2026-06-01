import os
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from app.core.config import settings

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Firebase mock or real verification (Assuming real is implemented with firebase_admin)
import firebase_admin
from firebase_admin import credentials, auth

# Initialize firebase in main.py or dependencies, but here's a helper
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None
