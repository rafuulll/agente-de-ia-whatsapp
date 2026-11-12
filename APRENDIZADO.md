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

# 11/11/2026

## 1. O que fiz
Criei a verificação e o recebimento do webhook da Meta, os testes automáticos e liguei tudo à Meta por um túnel.

GET /webhook - A Meta chama essa rota quando cadastro a URL. Ela manda hub.mode, hub.verify_token e hub.challenge. Se o modo é "subscribe" e o token é igual ao do meu .env, devolvo o challenge como texto puro. Se não, devolvo 403.
POST /webhook - Recebe o JSON das mensagens, mostra no terminal e responde {"status": "ok"} com 200.

test_webhook - Três testes: GET com token certo (200 e corpo igual ao challenge), GET com token errado (403) e POST (200 e {"status": "ok"}).

Configurei o ngrok para ter uma URL pública, criei o app na Meta com o número de teste, cadastrei o webhook com essa URL e assinei o campo messages. O evento de exemplo da Meta chegou no meu servidor com 200.

Decisões registradas no DECISIONS.md: os dados reais da profissional ficam fora do repositório público (servicos.json no .gitignore e servicos.exemplo.json no Git) e mantenho dois diários, o APRENDIZADO.md (o que aprendi) e o DECISIONS.md (o que decidi e por quê).

## 2. Por que assim
O FastAPI entrega os parâmetros da URL como parâmetros da função. Como hub.mode tem ponto no nome, usei Query(alias="hub.mode").
O POST usa async def e await request.json() porque ler o corpo da requisição espera os dados chegarem.
O túnel é necessário porque meu servidor está em 127.0.0.1, endereço que só existe no meu computador. A Meta precisa de um endereço público.
O token de verificação fica no .env e é lido pelo pydantic-settings (config.py). Nunca vai no código nem no GitHub.

## 3. O que errei
- Deixei o alias com espaços em vez de "hub.mode": a rota respondeu 422 (parâmetro obrigatório ausente).
- Devolvi o challenge com return challenge: o FastAPI converte para JSON e o texto saiu entre aspas ("123"). O teste pegou: '"123"' == '123'. Corrigi com PlainTextResponse.
- Esqueci de importar o Query (NameError) e escrevi META_VERIFY_TOKEN sem aspas e sem importar (NameError). No config.py o campo é só meta_verify_token: str, e o valor vem do .env.
- Confundi o que o teste manda (params e json) com o que ele confere (assert).
- Escrevi 405 no lugar de 403 no teste do token errado.

## 4. O que descobri sobre o envio de mensagens
A mensagem de teste enviada pelo painel da Meta falhou com o erro 130497 (conta restrita de enviar mensagens para usuários neste país). Ainda não sei a causa exata. Minha hipótese é que o problema seja o envio por template com o número de teste, e não o recebimento. Vou testar amanhã enviando texto livre pela API, logo depois de receber um "oi". O custo das mensagens da Meta também fica em aberto: preciso confirmar na página oficial de preços antes de ligar o número real.

## 5. Respostas das três perguntas de recuperação

1. Por que o challenge precisa voltar sem aspas e o que usei?
O FastAPI converte tudo que a rota devolve para JSON, e um texto em JSON vem entre aspas. A Meta compara o corpo da resposta com o número que ela mandou, então tem que ser o texto puro. Usei PlainTextResponse para devolver o texto sem converter.

2. Onde está o texto da mensagem e o remetente no JSON da Meta?
Texto: corpo["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
Remetente (número): corpo["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

3. Por que o POST responde 200 logo, antes de processar?
Se a Meta não recebe o 200 rápido, ela entende que falhou e reenvia a mesma mensagem. Responder logo evita isso, e o processamento (agenda, resposta) continua em seguida. A consequência é que a mesma mensagem pode chegar mais de uma vez, então o servidor vai precisar ser idempotente (não agendar duas vezes). Isso está previsto para a V3.
