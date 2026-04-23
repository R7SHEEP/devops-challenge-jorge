
# DevOps Challenge — FastAPI + Docker + Kubernetes

API REST segura construida con FastAPI, containerizada con Docker, orquestada con Kubernetes y con pipeline CI/CD en GitHub Actions.

## Producción

La API está desplegada y accesible en:

https://devops-challenge-jorge.onrender.com

## Arquitectura

```
Cliente HTTP
    │
    ▼
Nginx (Load Balancer)
    │
    ├──▶ API Instance 1 (FastAPI / Uvicorn)
    └──▶ API Instance 2 (FastAPI / Uvicorn)
```

**Stack tecnológico:**
- Python 3.11 + FastAPI + Uvicorn
- Autenticación: API Key + JWT único por transacción
- Docker + docker-compose (load balancer con Nginx)
- Kubernetes (Deployment + Service + HPA)
- CI/CD: GitHub Actions (Build → Test → Deploy)
- Análisis estático: Ruff
- Testing: pytest + pytest-cov

---

## Endpoint

### `POST /DevOps`

**Headers requeridos:**

| Header | Valor |
|--------|-------|
| `X-Parse-REST-API-Key` | `2f5ae96c-b558-4c7b-a590-a501ae1c3f6c` |
| `X-JWT-KWY` | `<tu JWT>` |
| `Content-Type` | `application/json` |

**Body:**
```json
{
  "message": "This is a test",
  "to": "Juan Perez",
  "from": "Rita Asturia",
  "timeToLifeSec": 45
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Hello Juan Perez your message will be sent",
  "jwt": "<JWT único generado por esta transacción>"
}
```

**Cualquier otro método HTTP → responde:** `ERROR`

---

## Correr localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn app.main:app --reload
```

**curl de prueba:**
```bash
curl -X POST \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: test-jwt" \
  -H "Content-Type: application/json" \
  -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
  http://localhost:8000/DevOps
```

---

## Docker + Load Balancer

```bash
# Levantar con 2 instancias + Nginx
docker-compose up --build

# La API queda disponible en:
http://localhost:80/DevOps
```

---

## Kubernetes

```bash
# Aplicar manifiestos
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Ver pods corriendo (mínimo 2)
kubectl get pods

# Escalar manualmente
kubectl scale deployment devops-api --replicas=4

# Acceder (Minikube)
minikube service devops-api-service
```

---

## Tests

```bash
# Correr todos los tests con cobertura
pytest tests/ --cov=app --cov-report=term-missing -v
```

---

## Análisis estático

```bash
ruff check app/
```

---

## CI/CD Pipeline (GitHub Actions)

El pipeline se activa automáticamente en cada push:

| Stage | Descripción |
|-------|-------------|
| **Build** | Instala dependencias y construye imagen Docker |
| **Test** | Análisis estático (ruff) + tests con cobertura |
| **Deploy** | Se ejecuta **solo en rama `master`** |

---

## Seguridad

- API Key validada en cada request via header `X-Parse-REST-API-Key`
- JWT único por transacción generado con `python-jose` (campo `jti` = UUID v4)
- Separación de responsabilidades: `auth.py` / `models.py` / `main.py`