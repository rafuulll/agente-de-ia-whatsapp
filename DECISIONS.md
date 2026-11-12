# Decisões do projeto

Cada decisão importante do projeto fica registrada aqui, com o motivo.

Modelo:

    ## NNN. Título curto
    Data:
    Contexto:
    Opções:
    Decisão:
    Por quê:
    Consequência:

---

## 001. Dados reais da profissional fora do repositório público
Data: 11/11/2026

Contexto: o repositório é público e os dados reais da profissional (serviços, preços, telefone, Instagram, endereço do salão) são informações de um negócio real.

Opções:
- A: commitar os dados reais.
- B: usar só dados fictícios em todo o projeto.
- C: commitar um arquivo de exemplo e manter o arquivo real fora do Git.

Decisão: opção C. O `servicos.exemplo.json` vai para o repositório e o `servicos.json` real fica no `.gitignore`.

Por quê: o projeto continua rodável por quem clonar (basta copiar o exemplo), e os dados dela não ficam expostos publicamente.

Consequência: a rota `/servicos` ainda usa uma lista fixa fictícia no `main.py`. Ler o arquivo `servicos.json` (com fallback para o exemplo) fica para a V1, com teste próprio.

---

## 002. Nome do arquivo de diário
Data: 11/11/2026

Contexto: o projeto tem o `APRENDIZADO.md` (diário do que fiz e errei) e agora o `DECISIONS.md` (decisões técnicas).

Decisão: manter os dois, cada um com uma função. `APRENDIZADO.md` conta o que aprendi no dia. `DECISIONS.md` registra escolhas e motivos.

Por quê: misturar os dois dificulta achar uma decisão depois.

Consequência: nenhuma além de lembrar de atualizar o arquivo certo.

---

## 003. Fechar a V0 sem resposta automática e sem proteção contra mensagem duplicada
Data: 12/11/2026

Contexto: a V0 é o servidor que recebe as mensagens da Meta pelo webhook (verificação por GET e recebimento por POST), com testes e túnel ngrok funcionando. O plano pedia fechar a V0 com a tag `v0` antes de começar a V1.

Opções:
- A: continuar na V0 até ela responder pela API e tratar mensagem repetida.
- B: fechar a V0 só com o recebimento e registrar o que falta.

Decisão: opção B. A V0 foi para a `main` pelo PR #1 e recebeu a tag `v0`, que está no GitHub.

Por quê: versões pequenas e fechadas deixam o histórico claro e evitam misturar assuntos num mesmo PR.

Consequência: a V0 ainda não responde pela API da Meta e não evita processar a mesma mensagem duas vezes (a Meta pode reenviar). A resposta pela API fica para as próximas versões e a proteção contra duplicata (idempotência) para a V3.

---

## 004. Serviços validados com Pydantic na leitura do arquivo
Data: 12/11/2026

Contexto: a rota `/servicos` devolvia uma lista fixa no `main.py`. Os serviços reais dela estão no `servicos.json`, que não vai para o Git (decisão 001).

Opções:
- A: validar só na saída da rota.
- B: validar cada item na leitura do arquivo e também declarar o formato da resposta da rota.

Decisão: opção B. O modelo `Servico` (`id` int, `nome` str, `duracao_min` int, `preco` float) fica em `app/models.py`. O `carregar_servicos()` em `app/servicos.py` lê o `servicos.json` (se não existir, usa o `servicos.exemplo.json`) e cria um `Servico` para cada item. A rota usa `response_model=list[Servico]`.

Por quê: se o arquivo estiver errado (campo faltando ou tipo trocado), o erro aparece na hora de ler, e não depois, quando o agente já estiver respondendo uma cliente. O `id` ficou int para não parecer igual ao nome.

Consequência: um JSON inválido derruba a leitura com `ValidationError`. Os testes usam dados falsos (`monkeypatch` na rota e `tmp_path` no leitor), então não dependem do arquivo real dela e passam em qualquer máquina. O erro ainda não diz qual arquivo falhou, o que fica no backlog. O preço está como float; se precisar de cálculo financeiro preciso, avaliar Decimal.
