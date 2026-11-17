from app import agente
from app.models import Servico


def test_montar_prompt_tem_preco_formatado(monkeypatch):
    falsos = [Servico(id=1, nome="Design de sobrancelhas", duracao_min=30, preco=40.0)]
    monkeypatch.setattr(agente, "carregar_servicos", lambda: falsos)
    prompt = agente.montar_prompt()
    assert "- Design de sobrancelhas: R$ 40,00, 30 min" in prompt


class RespostaFalsa:
    text = "resposta de mentira"


class ModelosFalsos:
    def generate_content(self, model, contents, config):
        return RespostaFalsa()


class ClienteFalso:
    def __init__(self, api_key):
        self.models = ModelosFalsos()


def test_responder_devolve_o_texto_do_modelo(monkeypatch):
    monkeypatch.setattr(agente.genai, "Client", ClienteFalso)
    assert agente.responder("oi") == "resposta de mentira"

def test_montar_conteudos_com_historico():
    historico = [("cliente", "quero cílios"), ("agente", "temos fio a fio")]
    conteudos = agente.montar_conteudos(historico, "quanto custa?")
    assert conteudos == [
        {"role": "user", "parts": [{"text": "quero cílios"}]},
        {"role": "model", "parts": [{"text": "temos fio a fio"}]},
        {"role": "user", "parts": [{"text": "quanto custa?"}]},
    ]

def test_montar_conteudo_sem_historico():
    historico = []
    conteudos = agente.montar_conteudos(historico, "quanto custa?")
    assert conteudos == [
        {"role": "user", "parts": [{"text": "quanto custa?"}]}
    ]