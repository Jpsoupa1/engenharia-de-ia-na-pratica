---
name: handoff
description: Grava decisões, estado e próximos passos numa nota de sessão antes de compactar ou limpar o contexto. Use antes de /compact ou /clear, ao parar no meio de uma tarefa, ou quando o contexto estiver longo.
---

<!-- Conceito: persistir, uma das quatro alavancas de contexto. O modelo não tem estado, mas o vault tem. -->

# Handoff

1. Copie `vault_exemplo/templates/sessao.md` para `vault_exemplo/sessoes/AAAA-MM-DD_<tarefa>.md`.
2. Preencha cada seção com o que outra sessão precisaria para continuar **sem reler a conversa**:
   * **Objetivo:** a tarefa em uma frase e a esteira.
   * **Decisões:** o que foi decidido e por quê (uma linha cada). Decisão difícil de reverter vira ADR em `vault_exemplo/decisoes/`.
   * **Estado:** o que está pronto, o que está pela metade, branch e último commit.
   * **Próximos passos:** lista curta, na ordem.
   * **Lições:** se houve erro repetido, use a skill `registrar-licao`.
3. Não copie trechos longos de código nem saída de comando: aponte o arquivo e a linha.
4. Nunca grave segredo, token ou dado pessoal na nota.
5. Diga ao humano o caminho da nota e que já pode rodar `/compact` ou `/clear`.
