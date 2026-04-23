import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_HEADERS = {
    "X-Parse-REST-API-Key": "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c",
    "X-JWT-KWY": "any-initial-jwt",
    "Content-Type": "application/json",
}

VALID_BODY = {
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45,
}


# ──────────────────────────────────────────────
# Tests del endpoint POST /DevOps
# ──────────────────────────────────────────────

def test_post_devops_success():
    """Debe retornar 200 y el mensaje correcto."""
    response = client.post("/DevOps", headers=VALID_HEADERS, json=VALID_BODY)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Juan Perez your message will be sent"


def test_post_devops_returns_jwt():
    """La respuesta debe incluir un JWT único."""
    response = client.post("/DevOps", headers=VALID_HEADERS, json=VALID_BODY)
    data = response.json()
    assert "jwt" in data
    assert len(data["jwt"]) > 0


def test_post_devops_jwt_is_unique_per_transaction():
    """Cada llamada debe generar un JWT diferente."""
    r1 = client.post("/DevOps", headers=VALID_HEADERS, json=VALID_BODY)
    r2 = client.post("/DevOps", headers=VALID_HEADERS, json=VALID_BODY)
    assert r1.json()["jwt"] != r2.json()["jwt"]


def test_post_devops_invalid_api_key():
    """Debe retornar 401 con API Key incorrecta."""
    bad_headers = {**VALID_HEADERS, "X-Parse-REST-API-Key": "invalid-key"}
    response = client.post("/DevOps", headers=bad_headers, json=VALID_BODY)
    assert response.status_code == 401


def test_post_devops_missing_api_key():
    """Debe retornar 422 si falta el header de API Key."""
    headers = {"X-JWT-KWY": "test", "Content-Type": "application/json"}
    response = client.post("/DevOps", headers=headers, json=VALID_BODY)
    assert response.status_code == 422


def test_post_devops_missing_jwt_header():
    """Debe retornar 400 si falta el header X-JWT-KWY."""
    headers = {
        "X-Parse-REST-API-Key": "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c",
        "Content-Type": "application/json",
    }
    response = client.post("/DevOps", headers=headers, json=VALID_BODY)
    assert response.status_code == 400


def test_post_devops_missing_body_field():
    """Debe retornar 422 si falta un campo requerido en el body."""
    bad_body = {"message": "test", "to": "Juan"}  # Falta 'from' y 'timeToLifeSec'
    response = client.post("/DevOps", headers=VALID_HEADERS, json=bad_body)
    assert response.status_code == 422


# ──────────────────────────────────────────────
# Tests de métodos HTTP no permitidos → ERROR
# ──────────────────────────────────────────────

def test_get_devops_returns_error():
    response = client.get("/DevOps")
    assert response.text == "ERROR"


def test_put_devops_returns_error():
    response = client.put("/DevOps")
    assert response.text == "ERROR"


def test_delete_devops_returns_error():
    response = client.delete("/DevOps")
    assert response.text == "ERROR"


# ──────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}