from fastapi import FastAPI, Header, HTTPException
from app.auth import create_token, verify_token

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login")
def login():
    token = create_token("jorge")
    return {"access_token": token}

@app.get("/secure")
def secure(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Falta token")

    try:
        token = authorization.split(" ")[1]
        payload = verify_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido")

        return {"message": "Acceso permitido", "user": payload["sub"]}

    except:
        raise HTTPException(status_code=401, detail="Error en autenticación")