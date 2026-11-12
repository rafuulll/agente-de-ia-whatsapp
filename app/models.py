from pydantic import BaseModel

class Servico(BaseModel):
    id: int
    nome: str
    duracao_min: int
    preco: float