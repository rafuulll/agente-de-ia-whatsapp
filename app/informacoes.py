from app.servicos import RAIZ


def carregar_informacoes() -> str:
    caminho = RAIZ / "informacoes.md"
    if not caminho.exists():
        caminho = RAIZ / "informacoes.exemplo.md"
    return caminho.read_text(encoding="utf-8")
