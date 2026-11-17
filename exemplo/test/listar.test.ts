// Conceito: verificação. São estes testes que o hook lint_e_testes.py roda depois de cada edição.

import { describe, expect, it } from "vitest";
import { filtrarPorStatus, listar } from "../src/listar.js";
import { criarTarefa, tarefasDeExemplo } from "../src/tarefas.js";

describe("listar", () => {
  it("ordena por data e depois por id", () => {
    const tarefas = [
      criarTarefa(3, "C", "2026-11-05"),
      criarTarefa(1, "A", "2026-11-05"),
      criarTarefa(2, "B", "2026-11-01"),
    ];
    expect(listar(tarefas).map((t) => t.id)).toEqual([2, 1, 3]);
  });

  it("não altera a lista original", () => {
    const original = [criarTarefa(2, "B", "2026-11-09"), criarTarefa(1, "A", "2026-11-01")];
    listar(original);
    expect(original.map((t) => t.id)).toEqual([2, 1]);
  });

  it("devolve lista vazia para entrada vazia", () => {
    expect(listar([])).toEqual([]);
  });
});

describe("filtrarPorStatus", () => {
  it("devolve só as tarefas do status pedido", () => {
    const pendentes = filtrarPorStatus(tarefasDeExemplo, "pendente");
    expect(pendentes.map((t) => t.id)).toEqual([3, 4]);
  });

  it("devolve vazio quando nenhuma tarefa tem o status", () => {
    const tarefas = [criarTarefa(1, "A", "2026-11-01", "feita")];
    expect(filtrarPorStatus(tarefas, "fazendo")).toEqual([]);
  });
});

describe("criarTarefa", () => {
  it("recusa título vazio", () => {
    expect(() => criarTarefa(1, "   ", "2026-11-01")).toThrow("título");
  });

  it("recusa data fora do formato AAAA-MM-DD", () => {
    expect(() => criarTarefa(1, "A", "01/11/2026")).toThrow("Data inválida");
  });
});
