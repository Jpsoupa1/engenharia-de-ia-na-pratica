<!-- Conceito: esteira completa, orquestrador e workers, para trabalho grande, com mais portões porque o risco paga. -->
# Esteira completa

**Para:** trabalho de vários dias, com frentes independentes ou risco alto. Exemplo: trocar o armazenamento em memória por um banco, com autenticação e migração de dados.

Aqui o orquestrador entra, porque as subtarefas não dá para escrever de antemão. Cada agente a mais tem custo de tokens e de coordenação, então só vale se a tarefa paga.

## Ingredientes

* **Orquestrador.** Lê o plano, decide as subtarefas e distribui. Modelo maior (Opus), porque planeja.
* **Workers.** Implementam uma frente cada, em paralelo, cada um na sua worktree (`isolation: worktree`). Sonnet.
* **Revisor.** [revisor](../.claude/agents/revisor.md) confere cada entrega contra o plano e os critérios.
* **Segurança.** [seguranca](../.claude/agents/seguranca.md) (Opus, só leitura) audita as zonas sensíveis: auth, dados pessoais, dinheiro, infraestrutura. Veja o [checklist](../seguranca/checklist.md).
* **Evals.** [casos de avaliação](../evals/casos.md) rodados antes e depois, para saber se a mudança melhorou ou piorou.
* **Telemetria.** Os hooks gravam a sessão, e o [relatório](../observabilidade/README.md) mostra onde o tempo foi.

## Fluxo

1. **Spec e plano.** Critérios de aceite por frente. Você aprova.
2. **Divisão.** O orquestrador separa as frentes independentes e as dependentes.
3. **Ondas.** Até 3 workers em paralelo. As frentes dependentes esperam.
4. **Revisão por entrega.** Cada worker passa pelo revisor antes de integrar.
5. **Integração.** As branches entram numa branch do ciclo, com testes rápidos.
6. **Segurança.** Auditoria sobre o diff integrado.
7. **Evals.** Rodar os casos e comparar com a base.
8. **Aprovação e CI.** Você aprova, o CI roda, e só então vai para a staging.

## Limite de tempo por etapa

Cada etapa tem um teto de tempo de relógio, escrito no plano. Estourou, o orquestrador para e devolve o estado a você, em vez de continuar gastando. Sem teto, esta esteira é a que mais cresce sem ninguém perceber. Meça com a [observabilidade](../observabilidade/README.md).

## Portões

| Portão | Quem | Quando |
|---|---|---|
| Spec e plano | você | antes de qualquer código |
| Hooks | automático | a cada edição |
| Revisão | agente revisor | por entrega |
| Segurança | agente seguranca | no diff integrado |
| Evals | automático | antes do merge |
| Merge e CI | você e CI | no fim |

## Quando NÃO usar

* A tarefa cabe em uma frente só. Use a [padrão](padrao.md).
* Você sabe os passos de antemão. Isso é workflow, não precisa de orquestrador.
* As frentes dependem umas das outras o tempo todo. Paralelizar vira conflito de merge.
* Não há risco alto nem zona sensível. O custo de segurança e evals não se paga.
* Você não vai medir. Sem medir, não sabe se o custo valeu.

Lição da aula: uma tarefa de cerca de 3 horas passou a levar cerca de 15 quando todo o processo era usado em tudo. A correção veio de medir e escolher a esteira certa.

**Próximo problema:** como saber se a esteira está funcionando? Veja os [evals](../evals/README.md).
