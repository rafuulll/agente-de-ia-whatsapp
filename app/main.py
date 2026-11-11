from fastapi import FastAPI, Query, HTTPException
from app.config import settings

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/servicos")
def servicos():
    return [
    {"nome":"Extensão de cílios", "duracao_min": 90, "preco": 150},
    {"nome": "Design de sobrancelhas", "duracao_min": 40, "preco": 80},
    {"nome": "Brow lamination", "duracao_min": 60, "preco": 120}]

@app.get("/webhook")
def webhook(
    mode:str = Query(alias="hub.mode"), 
    token:str = Query(alias="hub.verify_token"), 
    challenge:str = Query(alias="hub.challenge")):

    if(mode == "subscribe" and token == settings.meta_verify_token):
        return challenge
    raise HTTPException(status_code=403, detail="Sem permissão")