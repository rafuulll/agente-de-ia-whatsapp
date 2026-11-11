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
