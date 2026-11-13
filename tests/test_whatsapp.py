from app.whatsapp import enviar_mensagem, extrair_mensagem


def test_extrai_numero_e_texto():
    corpo = {
        "entry": [{"changes": [{"value": {"messages": [{
            "from": "5515999990000",
            "type": "text",
            "text": {"body": "Quanto custa?"},
        }]}}]}]
    }
    assert extrair_mensagem(corpo) == ("5515999990000", "Quanto custa?")


def test_evento_de_status_sem_mensagem():
    corpo = {"entry": [{"changes": [{"value": {"statuses": [{"status": "read"}]}}]}]}
    assert extrair_mensagem(corpo) is None


def test_mensagem_que_nao_e_texto():
    corpo = {
        "entry": [{"changes": [{"value": {"messages": [{
            "from": "5515999990000",
            "type": "image",
        }]}}]}]
    }
    assert extrair_mensagem(corpo) is None


def test_json_qualquer():
    assert extrair_mensagem({"teste": "oi"}) is None


def test_enviar_mensagem_monta_a_requisicao(monkeypatch):
    capturado = {}

    class RespostaFalsa:
        status_code = 200
        text = "ok"

        def raise_for_status(self):
            pass

    def post_falso(url, headers, json, timeout):
        capturado["url"] = url
        capturado["headers"] = headers
        capturado["json"] = json
        return RespostaFalsa()

    monkeypatch.setattr("app.whatsapp.httpx.post", post_falso)
    monkeypatch.setattr("app.whatsapp.settings.meta_phone_number_id", "123")
    monkeypatch.setattr("app.whatsapp.settings.meta_access_token", "token-falso")

    enviar_mensagem("5515999990000", "Oi!")

    assert capturado["url"].endswith("/123/messages")
    assert capturado["headers"]["Authorization"] == "Bearer token-falso"
    assert capturado["json"]["to"] == "5515999990000"
    assert capturado["json"]["text"]["body"] == "Oi!"
