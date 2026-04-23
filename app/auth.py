import time
import uuid

from fastapi import Header, HTTPException
from jose import jwt

API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
SECRET = "mysecret-devops-challenge"
ALGORITHM = "HS256"


def validate_api_key(x_parse_rest_api_key: str = Header(...)):
    if x_parse_rest_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


def generate_jwt() -> str:
    """Genera un JWT único por transacción usando jti (JWT ID)."""
    payload = {
        "iat": int(time.time()),
        "jti": str(uuid.uuid4()),  # ID único por transacción
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)