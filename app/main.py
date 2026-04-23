from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import JSONResponse, PlainTextResponse
 
from app.models import MessageRequest
from app.auth import validate_api_key, generate_jwt
 
app = FastAPI(title="DevOps Challenge API")
 
 
@app.post("/DevOps")
def devops_endpoint(
    request: MessageRequest,
    api_key: str = Depends(validate_api_key),
    x_jwt_kwy: str = Header(None),
):
    if not x_jwt_kwy:
        raise HTTPException(status_code=400, detail="JWT required in X-JWT-KWY header")
 
    # Genera un JWT único por transacción
    transaction_jwt = generate_jwt()
 
    # Devuelve EXACTAMENTE el JSON solicitado en el cuerpo, y el JWT en los headers
    return JSONResponse(
        content={
            "message": f"Hello {request.to} your message will be sent"
        },
        headers={
            "X-Transaction-JWT": transaction_jwt
        }
    )
 
 
@app.api_route("/DevOps", methods=["GET", "PUT", "DELETE", "PATCH"])
def invalid_method():
    return PlainTextResponse("ERROR")
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}