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