from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import PlainTextResponse
from app.config import settings
from app.models import Servico
from app.servicos import carregar_servicos

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/servicos", response_model=list[Servico])
def servicos():
    return carregar_servicos()

@app.get("/webhook")
def webhook(
    mode:str = Query(alias="hub.mode"), 
    token:str = Query(alias="hub.verify_token"), 
    challenge:str = Query(alias="hub.challenge")):

    if(mode == "subscribe" and token == settings.meta_verify_token):
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="Sem permissão")

@app.post("/webhook")
async def receber_mensagem(request: Request):
    corpo = await request.json()

    print(corpo)
    return {"status":"ok"}