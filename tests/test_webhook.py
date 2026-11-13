from fastapi.testclient import TestClient
from app.config import settings
from app.main import app

client = TestClient(app)

def test_get_webhook_token_certo():
    response = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": settings.meta_verify_token,
        "hub.challenge": "123",
    })

    assert response.status_code == 200
    assert response.text == "123"


def test_get_webhook_token_errado():
    response = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "errado",
        "hub.challenge": "123",
    })

    assert response.status_code == 403


def test_post_webhook():
    response = client.post("/webhook", json={"teste":"oi"})

    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_post_mensagem_de_texto_chama_o_agente(monkeypatch):
    chamadas = []

    def responder_falso(texto):
        chamadas.append(texto)
        return "resposta falsa"

    enviadas = []
    monkeypatch.setattr("app.main.responder", responder_falso)
    monkeypatch.setattr(
        "app.main.enviar_mensagem", lambda numero, texto: enviadas.append((numero, texto))
    )
    corpo = {
        "entry": [{"changes": [{"value": {"messages": [{
            "from": "5515999990000",
            "type": "text",
            "text": {"body": "Quanto custa?"},
        }]}}]}]
    }

    response = client.post("/webhook", json=corpo)

    assert response.status_code == 200
    assert chamadas == ["Quanto custa?"]
    assert enviadas == [("5515999990000", "resposta falsa")]


def test_post_evento_de_status_nao_chama_o_agente(monkeypatch):
    chamadas = []
    monkeypatch.setattr("app.main.responder", lambda texto: chamadas.append(texto))
    corpo = {"entry": [{"changes": [{"value": {"statuses": [{"status": "read"}]}}]}]}

    response = client.post("/webhook", json=corpo)

    assert response.status_code == 200
    assert chamadas == []