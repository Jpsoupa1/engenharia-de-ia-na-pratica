---
name: registrar-licao
description: Aplica a regra da catraca quando um erro se repete. Decide se a correção vira uma linha no CLAUDE.md, um teste ou um hook, e registra a lição. Use quando o mesmo erro aparecer pela segunda vez, ou quando o humano disser "isso de novo".
---

<!-- Conceito: regra da catraca. Um erro que se repete vira proteção permanente e não volta mais. -->

# Registrar lição

## 1. Descreva o erro em uma frase
O que aconteceu, onde, e qual foi a correção.

## 2. Escolha o degrau mais forte que se paga

| Se o erro é... | Vira | Por quê |
|---|---|---|
| verificável por código e barato de checar | **hook** em `.claude/hooks/` | roda sempre, o modelo não esquece |
| um comportamento do código | **teste** em `exemplo/test/` | quebra no CI se voltar |
| um julgamento, convenção ou contexto | **uma linha** no `CLAUDE.md` ou no `AGENTS.md` | o agente lê em toda sessão |

Prefira hook a teste, e teste a instrução. Instrução no prompt é a proteção mais fraca: é a única que o modelo pode ignorar.

## 3. Aplique e prove
* Hook ou teste: mostre ele falhando no erro antigo e passando na correção.
* Linha no CLAUDE.md: uma frase, imperativa, sem histórico. O CLAUDE.md continua abaixo de 60 linhas; se passar, mova algo para uma skill.

## 4. Registre
Acrescente uma linha na nota de sessão (template em `vault_exemplo/templates/sessao.md`), seção "Lições":

```
<data> · <tecnologia> · <erro em poucas palavras> → virou <hook | teste | regra> em <arquivo>
```
