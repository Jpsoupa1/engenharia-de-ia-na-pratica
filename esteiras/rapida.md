<!-- Conceito: esteira rápida, um agente, um loop curto, com o humano revisando o diff. -->
# Esteira rápida

**Para:** tarefas de menos de 1 hora, com passos conhecidos e risco baixo. Exemplo: corrigir `filtrarPorStatus` que ignora um status, ou ajustar uma mensagem.

## Ingredientes

* **Um agente.** O principal faz tudo. Sem subagentes, sem plano escrito.
* **CLAUDE.md** curto com os comandos de teste e as convenções que o código não mostra. Ver [CLAUDE.md](../CLAUDE.md).
* **Hook de testes.** [lint_e_testes.py](../.claude/hooks/lint_e_testes.py) roda biome e os testes afetados a cada edição em `exemplo/`. Se falha, o erro volta ao agente, que corrige no próprio loop.
* **Humano revisa o diff.** É o único portão manual.

## Passos

1. Descreva o problema em duas ou três frases, com o critério de aceite.
2. O agente lê só o que precisa (grep antes de abrir arquivo), edita e roda os testes.
3. O hook devolve qualquer falha, e o agente corrige.
4. Você lê o diff inteiro.
5. Commit e CI.

## Portões

| Portão | Quem | O que verifica |
|---|---|---|
| Hook de testes | automático | lint e testes do arquivo editado |
| Diff | você | o que mudou é só o que foi pedido |
| CI | automático | lint, typecheck e testes completos |

## Modelo

Sonnet implementa. Se a tarefa pede Opus, ela provavelmente não é rápida: refaça a triagem.

## Sinais de que subiu de tamanho

* O agente precisou investigar mais de dois arquivos que você não previa.
* Surgiu uma decisão de design que merece plano.
* O diff passou de umas poucas dezenas de linhas.

Pare e vá para a [esteira padrão](padrao.md), com a justificativa escrita.

**Próximo problema:** a tarefa precisa de investigação e de um plano aprovado. Veja a [esteira padrão](padrao.md).
