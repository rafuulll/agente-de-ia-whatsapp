from app.whatsapp import extrair_mensagem


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