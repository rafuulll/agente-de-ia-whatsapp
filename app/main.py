from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import PlainTextResponse
from app.agente import responder
from app.config import settings
from app.models import Servico
from app.servicos import carregar_servicos
from app.whatsapp import enviar_mensagem, extrair_mensagem

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

    resultado = extrair_mensagem(corpo)
    if resultado is None:
        return {"status": "ok"}

    numero, texto = resultado
    try:
        resposta = responder(texto)
        enviar_mensagem(numero, resposta)
    except Exception as erro:
        print("Erro ao atender a mensagem:", erro)

    return {"status": "ok"}
