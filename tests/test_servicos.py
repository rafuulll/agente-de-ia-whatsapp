import json
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from app import servicos
from app.main import app
from app.models import Servico

client = TestClient(app)

def test_servicos(monkeypatch):
    falsos = [
        Servico(id=1, nome="Servico A", duracao_min=30, preco=40.0),
        Servico(id=2, nome="Servico B", duracao_min=60, preco=80.0),
    ]
    monkeypatch.setattr("app.main.carregar_servicos", lambda: falsos)

    response = client.get("/servicos")

    assert response.status_code == 200
    dados = response.json()
    assert len(dados) == 2
    assert dados[0]["nome"] == "Servico A"

def test_carregar_servicos_dado_invalido(tmp_path, monkeypatch):
    arquivo = tmp_path / "servicos.json"
    arquivo.write_text(json.dumps([{"id": 1, "nome": "Sem preco", "duracao_min": 30}]), encoding="utf-8")
    monkeypatch.setattr("app.servicos.RAIZ", tmp_path)

    with pytest.raises(ValidationError):
        servicos.carregar_servicos()