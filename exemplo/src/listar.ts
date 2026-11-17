// Conceito: código alvo da esteira. O filtro por data NÃO existe de propósito: é a feature do exercício 5.

import type { Status, Tarefa } from "./tarefas.js";

/** Devolve uma cópia ordenada por data e, no empate, por id. Não altera a lista original. */
export function listar(tarefas: readonly Tarefa[]): Tarefa[] {
  return [...tarefas].sort((a, b) => a.data.localeCompare(b.data) || a.id - b.id);
}

/** Devolve só as tarefas com o status pedido, na mesma ordem de listar(). */
export function filtrarPorStatus(tarefas: readonly Tarefa[], status: Status): Tarefa[] {
  return listar(tarefas).filter((tarefa) => tarefa.status === status);
}
