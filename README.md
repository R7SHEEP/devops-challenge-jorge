# DevOps Challenge — FastAPI + Docker + Kubernetes

API REST segura construida con FastAPI, containerizada con Docker, orquestada con Kubernetes y con pipeline CI/CD en GitHub Actions.

---

## Informacion del Proyecto

| Campo | Valor |
|-------|-------|
| **Repositorio** | github.com/R7SHEEP/devops-challenge-jorge |
| **API en Produccion** | https://devops-challenge-jorge.onrender.com |
| **Endpoint** | POST /DevOps |
| **API Key** | 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c |
| **Cobertura Tests** | 100% (11 tests) |

---

## Arquitectura

```
Cliente HTTP
    │
    ▼
Nginx (Load Balancer / API Gateway)   ← Local y Kubernetes
    │
    ├──▶ API Instance 1 (FastAPI / Uvicorn :8000)
    └──▶ API Instance 2 (FastAPI / Uvicorn :8000)
```

> **Nota sobre produccion (Render):** El plan gratuito de Render no soporta
> docker-compose con multiples servicios. En produccion corre 1 instancia
> directamente desde el Dockerfile. El balanceador con 2 nodos esta disponible
> localmente con `docker-compose up --build` y en Kubernetes con `k8s/`.

**Stack tecnologico:**
- Python 3.11 + FastAPI + Uvicorn
- Autenticacion: API Key + JWT unico por transaccion (jti = UUID v4)
- Docker + docker-compose + Nginx (balanceador local)
- Kubernetes (Deployment 2 replicas + Service + HPA escalabilidad dinamica)
- CI/CD: GitHub Actions (Build → Test → Deploy)
- Analisis estatico: Ruff
- Testing: pytest + pytest-cov (100% cobertura)

---

## Endpoint

### `POST /DevOps`

**Headers requeridos:**

| Header | Valor |
|--------|-------|
| `X-Parse-REST-API-Key` | `2f5ae96c-b558-4c7b-a590-a501ae1c3f6c` |
| `X-JWT-KWY` | `<cualquier string>` |
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
  "jwt": "<JWT unico generado por esta transaccion>"
}
```

**Cualquier otro metodo HTTP (GET, PUT, DELETE, PATCH) responde:** `ERROR`

---

## Validacion del Evaluador

### Linux / macOS / Kali

```bash
curl -X POST \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: test-jwt-123" \
  -H "Content-Type: application/json" \
  -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
  https://devops-challenge-jorge.onrender.com/DevOps
```

### Windows (CMD / PowerShell)

```cmd
curl -X POST -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" -H "X-JWT-KWY: test-jwt-123" -H "Content-Type: application/json" -d "{\"message\":\"This is a test\",\"to\":\"Juan Perez\",\"from\":\"Rita Asturia\",\"timeToLifeSec\":45}" https://devops-challenge-jorge.onrender.com/DevOps
```

> **Nota cold start:** La primera solicitud puede tardar 30-60 segundos por el
> cold start del plan gratuito de Render. Las siguientes responden de inmediato.

---

## Correr Localmente (sin balanceador)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn app.main:app --reload
```

**Probar en localhost:8000:**

```bash
# Linux / macOS
curl -X POST \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: test-jwt" \
  -H "Content-Type: application/json" \
  -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
  http://localhost:8000/DevOps

# Windows
curl -X POST -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" -H "X-JWT-KWY: test-jwt" -H "Content-Type: application/json" -d "{\"message\":\"This is a test\",\"to\":\"Juan Perez\",\"from\":\"Rita Asturia\",\"timeToLifeSec\":45}" http://localhost:8000/DevOps
```

---

## Balanceador de Carga — 2 Nodos (Docker local)

Requiere **Docker Desktop** instalado: https://www.docker.com/products/docker-desktop

```bash
# Levantar Nginx + 2 instancias FastAPI
docker-compose up --build
```

Esto levanta 3 contenedores:
- `devops-api-1` — Instancia 1 en puerto 8000
- `devops-api-2` — Instancia 2 en puerto 8000
- `devops-lb` — Nginx Load Balancer en puerto 80

**Verificar contenedores activos:**

```bash
docker-compose ps
```

**Probar el balanceador (puerto 80 via Nginx):**

```bash
# Linux / macOS
curl -X POST \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: test-jwt-123" \
  -H "Content-Type: application/json" \
  -d '{"message":"This is a test","to":"Juan Perez","from":"Rita Asturia","timeToLifeSec":45}' \
  http://localhost/DevOps

# Windows
curl -X POST -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" -H "X-JWT-KWY: test-jwt-123" -H "Content-Type: application/json" -d "{\"message\":\"This is a test\",\"to\":\"Juan Perez\",\"from\":\"Rita Asturia\",\"timeToLifeSec\":45}" http://localhost/DevOps
```

---

## Kubernetes — Orquestacion y Escalabilidad

```bash
# Aplicar manifiestos
kubectl apply -f k8s/deployment.yaml   # 2 replicas + health probes
kubectl apply -f k8s/service.yaml      # NodePort puerto 80 -> 8000
kubectl apply -f k8s/hpa.yaml          # HPA: escala de 2 a 10 pods segun CPU

# Ver pods corriendo (minimo 2)
kubectl get pods

# Escalar manualmente
kubectl scale deployment devops-api --replicas=4

# Acceder (Minikube)
minikube service devops-api-service
```

---

## Tests Automatizados

```bash
# Correr todos los tests con cobertura
pytest tests/ --cov=app --cov-report=term-missing -v
```

Resultado esperado:

```
11 passed in 1.56s

Name            Stmts  Miss  Cover
-----------------------------------
app/auth.py        13     0   100%
app/main.py        17     0   100%
app/models.py       8     0   100%
-----------------------------------
TOTAL              38     0   100%
```

---

## Analisis Estatico

```bash
ruff check app/
```

---

## CI/CD Pipeline (GitHub Actions)

El pipeline se activa automaticamente en cada push:

| Stage | Descripcion | Condicion |
|-------|-------------|-----------|
| **Build** | Instala dependencias + construye imagen Docker | Todos los branches |
| **Test** | Ruff (analisis estatico) + pytest con cobertura | Todos los branches |
| **Deploy** | Tag de imagen + confirmacion de deploy | Solo rama `master` |

- Ejecucion bajo demanda: habilitada con `workflow_dispatch`
- Versionado: cada imagen se tagea con el SHA del commit (`github.sha`)

---

## Seguridad

- API Key validada en cada request via header `X-Parse-REST-API-Key`
- Retorna `401 Unauthorized` si la key es incorrecta
- JWT unico por transaccion generado con `python-jose` (campo `jti` = UUID v4)
- Separacion de responsabilidades: `auth.py` / `models.py` / `main.py`

---

## Gestor de API y Balanceador

- **Local**: Nginx actua como API Gateway y balanceador entre 2 instancias (`docker-compose`)
- **Kubernetes**: Service NodePort distribuye trafico entre 2+ replicas con HPA
- **Produccion**: Render.com con URL publica — arquitectura multi-nodo disponible en `docker-compose.yml` y `k8s/`

---

## TDD — Test Driven Development

Los tests cubren todos los casos del enunciado:
- Exito con JSON correcto y headers validos
- Validacion de API Key (correcta e incorrecta)
- JWT presente y unico por transaccion
- Metodos HTTP invalidos devuelven ERROR
- Campos faltantes en el body
- Health check del servicio

Cobertura final: **100%** en `auth.py`, `main.py` y `models.py`