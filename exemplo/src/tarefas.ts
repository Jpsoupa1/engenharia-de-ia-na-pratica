// Conceito: projeto de exemplo para praticar a esteira. Modelo de dados pequeno e sem dependências.

export type Status = "pendente" | "fazendo" | "feita";

export interface Tarefa {
  id: number;
  titulo: string;
  status: Status;
  /** Data no formato ISO AAAA-MM-DD. */
  data: string;
}

const DATA_ISO = /^\d{4}-\d{2}-\d{2}$/;

export function criarTarefa(id: number, titulo: string, data: string, status: Status = "pendente"): Tarefa {
  const tituloLimpo = titulo.trim();
  if (tituloLimpo === "") {
    throw new Error("O título não pode ser vazio.");
  }
  if (!DATA_ISO.test(data)) {
    throw new Error(`Data inválida: ${data}. Use AAAA-MM-DD.`);
  }
  return { id, titulo: tituloLimpo, status, data };
}

export const tarefasDeExemplo: readonly Tarefa[] = [
  criarTarefa(1, "Escrever o plano da feature", "2026-11-03", "feita"),
  criarTarefa(2, "Revisar o diff com o agente revisor", "2026-11-10", "fazendo"),
  criarTarefa(3, "Configurar o hook de testes", "2026-11-12"),
  criarTarefa(4, "Registrar a lição da semana", "2026-11-20"),
];
