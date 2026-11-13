


def extrair_mensagem(corpo: dict):
    try:
        valor = corpo["entry"][0]["changes"][0]["value"]
        mensagem = valor["messages"][0]
        if mensagem["type"] != "text":
            return None
        return mensagem["from"], mensagem["text"]["body"]
    except (KeyError, IndexError):
        return None

    