import httpx

from app.config import settings


def extrair_mensagem(corpo: dict):
    try:
        valor = corpo["entry"][0]["changes"][0]["value"]
        mensagem = valor["messages"][0]
        if mensagem["type"] != "text":
            return None
        return mensagem["from"], mensagem["text"]["body"]
    except (KeyError, IndexError):
        return None


def enviar_mensagem(numero: str, texto: str) -> None:
    url = (
        f"https://graph.facebook.com/{settings.meta_graph_version}"
        f"/{settings.meta_phone_number_id}/messages"
    )
    resposta = httpx.post(
        url,
        headers={"Authorization": f"Bearer {settings.meta_access_token}"},
        json={
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": texto},
        },
        timeout=10,
    )
    if resposta.status_code >= 400:
        print("Meta recusou o envio:", resposta.text)
    resposta.raise_for_status()
