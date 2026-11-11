from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/servicos")
async def servicos():
    return [
    {"nome":"Extensão de cílios", "duracao_min": 90, "preco": 150},
    {"nome": "Design de sobrancelhas", "duracao_min": 40, "preco": 80},
    {"nome": "Brow lamination", "duracao_min": 60, "preco": 120}]