from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_servicos():
    response = client.get("/servicos")
    dados = response.json()

    assert response.status_code == 200
    assert isinstance(dados, list)
    assert len(dados) == 3
    for item in dados:
        assert "nome" in item
        assert isinstance(item["nome"], str)