from google import genai
from google.genai import types

from app.config import settings
from app.informacoes import carregar_informacoes
from app.servicos import carregar_servicos
from app.prompt import PROMPT_SISTEMA



def montar_prompt() -> str:
    linhas = []
    for servico in carregar_servicos():
        preco = f"{servico.preco:.2f}".replace(".", ",")
        linhas.append(f"- {servico.nome}: R$ {preco}, {servico.duracao_min} min")
    return PROMPT_SISTEMA.format(
        nome_salao=settings.salao_nome,
        nome_profissional=settings.profissional_nome,
        servicos="\n".join(linhas),
        informacoes=carregar_informacoes(),
    )

def montar_conteudos(historico: list, texto: str) -> list:
    traducao = {"cliente": "user", "agente": "model"}
    conteudos = []
    for papel, mensagem in historico:
        conteudos.append({"role": traducao[papel], "parts": [{"text": mensagem}]})
    conteudos.append({"role": "user", "parts": [{"text": texto}]})
    return conteudos

def responder(texto_da_cliente: str, historico=None) -> str:
    if historico is None:
        historico = []
    cliente = genai.Client(api_key=settings.gemini_api_key)
    resposta = cliente.models.generate_content(
        model=settings.gemini_model,
        contents=montar_conteudos(historico, texto_da_cliente),
        config=types.GenerateContentConfig(system_instruction=montar_prompt()),
    )
    return resposta.text
