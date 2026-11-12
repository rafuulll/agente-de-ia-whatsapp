import json
from pathlib import Path
from app.models import Servico

RAIZ = Path(__file__).resolve().parent.parent

def carregar_servicos() -> list[Servico]:
    caminho = RAIZ / "servicos.json"
    if not caminho.exists():
        caminho = RAIZ / "servicos.exemplo.json"
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return [Servico(**item) for item in dados]