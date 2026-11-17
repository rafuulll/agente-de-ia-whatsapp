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


# 12/11/2026

## 1. O que fiz
Fechei a V0 e fiz a V1: os serviços agora vêm de um arquivo e são validados com Pydantic.

V0 - O código do webhook foi para a main pelo PR #1 e criei a tag v0, que confirmei no GitHub com git ls-remote --tags origin.
Servico (app/models.py) - Classe Pydantic com id (int), nome (str), duracao_min (int) e preco (float).
carregar_servicos() (app/servicos.py) - Lê o servicos.json e, se ele não existir, usa o servicos.exemplo.json. Cada item vira um Servico(**item), então o Pydantic valida na leitura.
GET /servicos - Passou a usar o carregar_servicos() e declara response_model=list[Servico].
servicos.json real - Preenchi com os 24 serviços dela. Ele está no .gitignore e não sobe para o GitHub.

Testes novos (agora são 6 passando):
test_servicos - Troca a função carregar_servicos por uma com 2 serviços falsos (monkeypatch) e confere status 200, 2 itens e o nome do primeiro.
test_carregar_servicos_dado_invalido - Cria uma pasta temporária (tmp_path) com um servicos.json sem o campo preco, troca a RAIZ por ela e espera ValidationError (pytest.raises).

Também escrevi no DECISIONS.md a 003 (V0 fechada sem resposta pela API e sem proteção contra mensagem duplicada) e a 004 (validação na leitura do arquivo, id int e testes com dados falsos), e criei um modelo de pull request (.github/pull_request_template.md).

## 2. Por que assim
A classe Servico serve para manter um padrão: sem ela, o serviço seria qualquer dicionário solto. Com ela, todo serviço precisa ter id, nome, duracao_min e preco.
O Pydantic valida na leitura do arquivo para o erro aparecer na hora, e não depois, quando o agente já estiver respondendo uma cliente.
O id é int para não ficar parecido com o nome.
O teste da rota não usa o servicos.json real porque ele não está no GitHub e muda quando o catálogo muda. Trocando a função leitora por uma com dados falsos, o teste dá o mesmo resultado em qualquer máquina e só falha se a rota quebrar.
O monkeypatch troca a RAIZ (a pasta) e não o arquivo, porque o leitor monta o caminho juntando a pasta com o nome do arquivo, e só a pasta é uma variável que dá para trocar.

## 3. O que errei
- Colei do chat aspas curvas no código e deu SyntaxError. No código só funcionam aspas retas.
- Escrevi responde_model em vez de response_model.
- Deixei os ids como texto no JSON de exemplo, mas o modelo pedia int. Decidi deixar tudo int.
- Esqueci imports no arquivo de testes (json, pytest e servicos), o que daria NameError.
- Achei que o Pydantic só devolvia os itens que batiam com a classe. Na verdade ele valida cada item: campo faltando ou tipo impossível dá ValidationError, e só campos a mais são ignorados.
- Achei que o monkeypatch trocava arquivos. Ele troca funções e variáveis, só durante o teste.

## 4. O que ainda não entendo bem
monkeypatch: entendi o que faz, mas preciso ver mais exemplos para explicar sem consultar. O mesmo vale para o ** (desempacotar o dicionário) no Servico(**item).

## 5. Respostas das três perguntas de recuperação

1. O que o Pydantic faz quando um campo chega com o tipo errado?
Ele tenta converter para o tipo declarado. Se der, segue (preco "40" vira 40.0). Se não der (preco "abc"), levanta ValidationError e o dado não passa.

2. Por que o teste de /servicos não pode depender do servicos.json real?
Porque o arquivo não está no repositório do GitHub e muda cada vez que alteramos ele. Então troco a função carregar_servicos por uma com dois serviços falsos usando monkeypatch, e o teste dá o mesmo resultado em todas as máquinas e só falha se a rota falhar.

3. Se a Meta reenviar a mesma mensagem, o que o servidor faz e o que falta?
A Meta reenvia o webhook se não receber 200 rápido ou se receber erro, então o servidor deve responder 200 rápido para ela não reenviar a mensagem. Hoje cada POST é tratado como uma mensagem nova, portanto o que falta é a idempotência: guardar o id de cada mensagem e, caso a Meta reenvie, identificar que já foi processada e não processar de novo, para evitar mensagens duplicadas.


# 13/11/2026

(Rascunho escrito com ajuda do Claude a pedido meu. Preciso ler tudo amanhã, corrigir o que não estiver com as minhas palavras e responder a seção 6 sozinho, sem consultar.)

## 1. O que fiz
Liguei o agente ao Gemini, liguei o webhook ao envio pela API da Meta e fiz o primeiro teste real de ponta a ponta. Descobri a causa do erro 130497.

Agente (app/agente.py) - montar_prompt() monta o prompt com o nome do salão, da profissional, a lista de serviços (nome, preço e duração) e o conteúdo do informacoes.md. responder(texto) chama o Gemini com esse prompt como instrução de sistema e devolve o texto da resposta.
informacoes (app/informacoes.py) - Lê o informacoes.md real e, se ele não existir, usa o informacoes.exemplo.md. Mesmo padrão do servicos.json: dado real fora do GitHub, exemplo dentro.
extrair_mensagem (app/whatsapp.py) - Recebe o JSON da Meta e devolve (número, texto). Se o JSON não tiver mensagem de texto (por exemplo, um aviso de status), devolve None. Feita com TDD, com 4 testes.
enviar_mensagem (app/whatsapp.py) - Faz um POST em graph.facebook.com/{versão}/{id do número}/messages com o token no cabeçalho Authorization e o texto no corpo. Se a Meta recusar, imprime o motivo e levanta erro.
POST /webhook (app/main.py) - Extrai a mensagem, chama o agente, envia a resposta e sempre devolve 200 para a Meta, mesmo se algo der erro no meio (o erro é impresso no terminal).
config - Novos campos: meta_access_token, meta_phone_number_id e meta_graph_version, lidos do .env.
Modelo - O gemini-2.5-flash-lite deu 404. Troquei no .env para o gemini-3.5-flash-lite (plano B: gemini-3.1-flash-lite).

Testes: agora são 15 passando (python -m pytest). O teste do agente usa um modelo falso, o do webhook usa um agente falso e um envio falso, e o do envio usa um httpx.post falso.

Teste real: subi o servidor com uvicorn, expus com ngrok, a Meta verificou o webhook (GET) e o botão de teste da Meta chegou no meu servidor (POST).

## 2. Por que assim
O nome do modelo fica no .env porque os modelos mudam de nome e de limite; assim troco sem mexer no código.
Os testes usam versões falsas do modelo, do envio e do httpx para não gastar cota, não depender de internet e dar sempre o mesmo resultado.
O POST sempre responde 200 porque, se a Meta não receber 200, ela reenvia a mesma mensagem. Por isso o erro é impresso, mas não devolvido.
extrair_mensagem devolve None quando não há texto porque a Meta manda também avisos de status (enviada, entregue, falhou), e o agente não deve responder a esses.
O token e o ID do número ficam no .env (que está no .gitignore) e o .env.example só tem os nomes.

## 3. O que errei
- Rodei pytest puro e deu "No module named app". O certo é python -m pytest, que põe a pasta do projeto no caminho.
- No JSON da Meta, esqueci o nível "changes" e o [0] dele ao montar o caminho até "messages".
- Subi o servidor antes de salvar o token no .env. O servidor só lê o .env quando liga, então o cabeçalho foi montado com o token vazio ("Illegal header value b'Bearer '"). Corrigi reiniciando o uvicorn.
- Tirei print do .env com a chave do Gemini e o token visíveis. Vou trocar a chave. Antes de qualquer print do .env, cubro as linhas das chaves.
- Entrei na tela errada do painel da Meta (Permissões e recursos) em vez de Etapa 2. Configuração da produção, onde ficam a URL de callback e o token de verificação.
- Minha hipótese do dia 11 sobre o 130497 (template, janela de 24 horas) estava errada.

## 4. O que ainda não entendo bem (confirmar amanhã e riscar o que já entendi)
Classes falsas nos testes (self, __init__, atributos criados por atribuição).
monkeypatch: onde trocar (onde o nome é usado, por exemplo app.main.responder).
raise_for_status e o que acontece com o código quando ele levanta erro.

## 5. A descoberta do dia: erro 130497 com causa confirmada
O envio do modelo de mensagem pelo painel foi aceito pela API, mas a mensagem não chegou. O motivo só apareceu no aviso de status que a Meta mandou depois pelo webhook: status "failed", código 130497, "Business account is restricted from messaging users in this country". Vi isso abrindo o painel do ngrok (127.0.0.1:4040), que guarda o corpo de cada requisição.
Causa: a Meta restringiu mensagens entre países para destinatários no Brasil (e na Indonésia), por causa de golpes. O número de teste é dos EUA (+1 555) e eu estava mandando para um número brasileiro.
Saída documentada: negócio com documentos legais do Brasil cria um portfólio empresarial da Meta no Brasil e migra o número para ele. Isso também vale para o salão real. O desbloqueio por "scaling path" não é garantido para o Brasil.
Consequência para o código: nosso servidor ignora avisos de status, então não registraria esse erro sozinho. Preciso passar a imprimir os status "failed" com o código do erro.
Sobre o 131030 que apareceu antes: era do teste de exemplo da Meta, com um número falso que não estava na minha lista de destinatários. Não tem relação com o 130497.

## 6. Perguntas de recuperação (responder amanhã, sem consultar)
1. Por que o servidor responde 200 mesmo quando o envio para a Meta falha, e qual o risco de fazer isso?
Resposta:

2. O que significava o erro "Illegal header value b'Bearer '" e por que reiniciar o servidor resolveu?
Resposta:

3. A API aceitou o envio, mas a mensagem não chegou. Como descobri o motivo e por que nosso código não mostrou o erro sozinho?
Resposta:

## 7. Pendências
- Trocar a chave do Gemini (apareceu em print).
- Passar a imprimir avisos de status "failed" com o código do erro (com teste).
- Falar com a profissional: ela tem CNPJ ou MEI? Tem um chip que não esteja em uso no WhatsApp? (depende disso o número real e o portfólio no Brasil.)
- Escrever a DECISIONS 005 (Gemini no plano gratuito, escolha do modelo, limites de privacidade).
- Subir os branches, abrir o PR com o modelo e conferir "Files changed" (nada de .env, servicos.json, informacoes.md, token).
- Ajustar o prompt: unificar o nome da profissional e tirar a promessa "vou avisar a profissional" até existir a transferência real.


# 15/11/2026

(Rascunho escrito com ajuda do Claude a pedido meu. Preciso ler tudo, corrigir o que não estiver com as minhas palavras e responder a seção 6 sozinho, sem consultar.)

## 1. O que fiz
Revisei o dia 13/11 (prova do fluxo com os 7 passos, prova dos arquivos de app/ e perguntas de recuperação), estudei SQLite e criei o módulo de memória da conversa com TDD.

Teoria de SQLite - conexão (a ligação com o arquivo do banco), cursor (o ponto de leitura de um comando), commit (grava de verdade o que estava em rascunho), fetchall (todas as linhas que faltam, em lista) e fetchone (a próxima linha, ou None). Fiz um mini exemplo fora do projeto (estudo_sqlite.py) e testei o que acontece sem o commit.
Branch feat/memoria-sqlite e *.db no .gitignore, porque o banco terá conversas reais.
Testes primeiro (tests/test_memoria.py, 3 testes): salva e busca na ordem, números diferentes não se misturam, limite devolve só as últimas. Rodei e deu vermelho (ModuleNotFoundError).
Código (app/memoria.py) - iniciar_banco(caminho) cria a tabela mensagens (id, numero, papel, texto); salvar_mensagem(caminho, numero, papel, texto) grava uma linha; buscar_historico(caminho, numero, limite=10) devolve as últimas mensagens daquele número, da mais antiga para a mais nova.
Resultado: 18 testes passando (os 15 de antes mais 3). Commit: feat: memoria da conversa em SQLite.
Escrevi também a decisão 006 no DECISIONS.md.

## 2. Por que assim
SQLite em vez de lista em memória ou Postgres: a lista some quando o uvicorn reinicia e não busca por número; o Postgres precisa de um servidor para manter, exagero para poucas conversas; o SQLite é um arquivo, já vem no Python e guarda os dados.
Cada função recebe o caminho do banco e abre a sua própria conexão, por isso o teste usa um banco temporário (tmp_path) e não mexe nos dados reais.
Os valores entram no SQL com ?, e nunca dentro de f-string, para ninguém mandar um comando por mensagem de WhatsApp (SQL injection).
Limite de 10 mensagens: histórico grande gasta tokens, deixa a resposta lenta e pode passar do limite de contexto do modelo.
A busca usa ORDER BY id DESC LIMIT para pegar as mais novas, e a função inverte a lista no fim, para o modelo ler a conversa em ordem cronológica.

## 3. O que errei
- Usei chaves { } no lugar de dois-pontos nas funções, e esqueci uma vírgula no CREATE TABLE.
- Tirei parâmetros do salvar_mensagem e coloquei valores dentro do sqlite3.connect; troquei o nome da tabela (mensagem em vez de mensagens).
- No SELECT escrevi ORDER BY id DESC and LIMIT == ?, e tirei o = 10 do parâmetro limite, o que quebraria as chamadas sem limite.
- No teste comparei com uma tupla em vez de uma lista de tuplas, deixei um assert sem comparação e inverti o resultado esperado para combinar com o SQL, quando o teste deve dizer o que a função deve devolver.
- Deixei uma vírgula dupla na tupla do exemplo de estudo.
- Achei que o commit servia para verificar SQL injection (ele só grava), e que conexão era para gravar e cursor para consultar (a conexão é a ligação, o cursor é o ponto de leitura).
- Achei que o id da mensagem poderia ficar numa variável; ela some quando o servidor reinicia.

## 4. O que ainda não entendo bem
Como explicar sozinho o "Bearer vazio" e como descobri o erro 130497 (preciso estudar as explicações que ficaram nas pendências do checklist).
Onde e como guardar o id da mensagem para a idempotência (ideia: no SQLite, uma coluna ou uma tabela de ids já processados).
Como devolver o 200 antes de chamar o Gemini (BackgroundTasks do FastAPI) e o que muda com os erros depois do 200.

## 5. A descoberta do dia
O commit é o que grava. Sem ele os dados ficam em rascunho e se perdem quando o programa fecha. E um teste escrito antes pega o erro de ordem do histórico, que seria fácil de esquecer.

## 6. Perguntas de recuperação (responder amanhã, sem consultar)
1. O que acontece com os dados se eu esquecer o commit(), e como testei isso?
Resposta:

2. Por que a buscar_historico usa DESC e depois inverte a lista?
Resposta:

3. Por que o webhook pode responder duas vezes à mesma mensagem da cliente, e como o SQLite poderia ajudar a evitar isso?
Resposta:

## 7. Pendências
- Ligar a memória ao agente e ao webhook (segunda, 16/11): hoje o responder recebe só o texto atual, sem o histórico.
- Idempotência (guardar o id de cada mensagem) e BackgroundTasks.
- Passar a imprimir os avisos de status failed com o código do erro (com teste).
- Estudar as explicações das respostas 3, 4, 5 e 8 e reescrevê-las com as minhas palavras; conferir a seção 1 do estudo do dia 13/11; responder a seção 6 do dia 13/11 e a de hoje.
- Reescrever o Por quê da decisão 006 com as minhas palavras; escrever a decisão 005 (Gemini).
- Perguntar à profissional se faz intervalo de almoço (o chip ela compra) e criar um Google Agenda meu, vazio, para testar a V2.
- Ajustar o prompt (unificar o nome da profissional; a promessa de avisar a profissional) e subir os branches com o PR, conferindo Files changed.
