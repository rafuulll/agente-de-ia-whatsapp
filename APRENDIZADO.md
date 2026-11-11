# 10/11/2026

## 1. O que fiz
Criei as rotas /health e /servicos e os testes para essas rotas (test_health e test_servicos)

GET /health - Verifica se o servidor está no ar
GET /servicos - Mostra os serviços.

test_health - Testa a rota /health verificando se o status code é 200 e se o corpo do json responde {"status":"ok"}
test_servicos - Testa a rota /servicos verificando se o status code é 200, a instância dados é do tipo lista, se possui 3 dicionários (foi a quantidade de serviços que criei), se existe a variável "nome" em cada dicionário e se essa variável "nome" é uma string.

## 2. Por que FastAPI
Escolhi o FastAPI porque é um framework moderno muito usado para API.
Ele gera a documentação da API de forma automática (/docs).
FastAPI transforma o que escrevi nas rotas em texto JSON automaticamente.

## 3. O que errei
Errei na hora de criar o return da rota /servicos, coloquei apenas um dicionario, e devia criar uma lista com 3 serviços (3 dicionários).
Também errei nos asserts do test_servicos na parte do for (for item in dados), mas o Claude me ajudou e me explicou o que devia ser feito. 