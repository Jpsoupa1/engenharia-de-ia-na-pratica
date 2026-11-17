<!-- Conceito: projeto de prática da esteira. Pequeno de propósito: o foco é o processo, não o código. -->

# Projeto de exemplo: lista de tarefas

Uma lista de tarefas em memória, em TypeScript, sem dependências de produção.

| Arquivo | O que tem |
|---|---|
| `src/tarefas.ts` | tipo `Tarefa` (id, título, status, data), `criarTarefa` e uma lista de exemplo |
| `src/listar.ts` | `listar` (ordena por data e id) e `filtrarPorStatus` |
| `test/listar.test.ts` | testes com Vitest |

## Comandos

```bash
npm install
npm test            # testes
npm run lint        # Biome
npm run typecheck   # TypeScript
npm run verificar   # os três juntos, é o que conta como "pronto"
```

## A tarefa: filtro por data

Esta feature **não está implementada**. Faça com a [esteira padrão](../esteiras/padrao.md), do plano ao merge (exercício 5 em [exercicios/](../exercicios/README.md)).

Crie `filtrarPorData(tarefas, { de?, ate? })` em `src/listar.ts`.

### Critérios de aceite
* [ ] Com `de` e `ate`, devolve só as tarefas com `de <= data <= ate`. Os limites entram.
* [ ] Só `de`: tudo a partir da data. Só `ate`: tudo até a data. Sem nenhum: o mesmo que `listar()`.
* [ ] A ordem é a mesma de `listar()`.
* [ ] A lista original não muda.
* [ ] Data fora do formato AAAA-MM-DD lança erro com a data na mensagem.
* [ ] `de` depois de `ate` lança erro.
* [ ] `npm run verificar` passa.

Tente escrever o seu plano antes de olhar o [plano de referência](../.claude/skills/planejar/exemplos/feature_filtro_data.md).

**Próximo problema:** com o código pronto, como saber quanto o processo custou? Veja [observabilidade/](../observabilidade/README.md).
