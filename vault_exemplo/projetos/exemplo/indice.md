---
tipo: indice
projeto: exemplo
estado: ativo
atualizado: 2026-11-16
tags: [projeto, exemplo]
---
<!-- Conceito: índice do projeto, o ponto de entrada que o agente lê primeiro. -->
# Projeto exemplo

## Resumo

Lista de tarefas em memória, em TypeScript, em `exemplo/`. A tarefa é `{ id, titulo, status, data }`, com status `pendente`, `fazendo` ou `feita`. Hoje existem `listar` e `filtrarPorStatus`. Falta `filtrarPorData(tarefas, { de?, ate? })`, que é o exercício da esteira padrão.

Comandos, dentro de `exemplo/`: `npm test`, `npm run lint`, `npm run typecheck`.

## Índice para agentes

Leia só o que a tarefa pedir.

* Por que a lista é em memória: [[decisoes/0001_exemplo]]
* Planejar uma tarefa padrão: [[templates/plano]]
* Registrar uma decisão difícil de reverter: [[templates/adr]]
* Registrar o fim de uma sessão: [[templates/sessao]]
* Sessões anteriores: pasta `sessoes/`, em ordem de data.

## Armadilhas conhecidas

* A data é uma string ISO `AAAA-MM-DD`, então a comparação de texto funciona, mas só se o formato for respeitado.
* `listar` não deve alterar o array recebido.

## Próximos passos

* Implementar o filtro por data.
* Decidir se a persistência sai da memória, o que pede um novo ADR.
