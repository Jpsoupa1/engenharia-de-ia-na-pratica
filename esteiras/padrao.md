<!-- Conceito: esteira padrão em oito passos, cada um ligado a um conceito e a um arquivo do repositório. -->
# Esteira padrão

**Para:** tarefas de 1 a 3 horas com alguma investigação. Exemplo da aula: o filtro por data, `filtrarPorData(tarefas, { de?, ate? })`, em `exemplo/`.

Um implementador, uma rodada de revisão, um CI. Nada de multiagente para tarefa que um agente resolve.

## Os oito passos

| # | Passo | Conceito | Arquivo que implementa |
|---|---|---|---|
| 1 | Contexto | selecionar o que entra no contexto | [CLAUDE.md](../CLAUDE.md), [vault_exemplo](../vault_exemplo/CLAUDE.md) |
| 2 | Plano | plano antes do código, critérios de aceite primeiro | [skill planejar](../.claude/skills/planejar/SKILL.md) |
| 3 | Aprovação do plano | portão humano | você lê o plano e diz sim |
| 4 | Implementação com subagente explorador | isolar a busca, higiene de contexto | [agente explorador](../.claude/agents/explorador.md) |
| 5 | Verificação por hooks | guardrail determinístico | [lint_e_testes.py](../.claude/hooks/lint_e_testes.py), [bloquear_perigosos.py](../.claude/hooks/bloquear_perigosos.py) |
| 6 | Revisão por agente | contexto limpo, só leitura | [agente revisor](../.claude/agents/revisor.md) e [skill revisar](../.claude/skills/revisar/SKILL.md) |
| 7 | Aprovação do merge | portão humano | você lê o diff e o relatório |
| 8 | CI | verificação independente do agente | [.github/workflows/ci.yml](../.github/workflows/ci.yml) |

## Passo a passo

### 1. Contexto
O agente começa com o `CLAUDE.md` curto. Para uma tarefa padrão, leia no máximo 3 notas do vault, ligadas à tarefa.

### 2. Plano
A skill `planejar` gera o plano no formato de [template_plano.md](../.claude/skills/planejar/template_plano.md). Veja um plano pronto em [feature_filtro_data.md](../.claude/skills/planejar/exemplos/feature_filtro_data.md). Os critérios de aceite vêm antes do código.

### 3. Aprovação do plano
Leia o plano. É o ponto mais barato para corrigir o rumo. Sem sim, nada é escrito.

### 4. Implementação com explorador
O agente principal implementa. Quando precisa entender uma área do código, chama o `explorador` (Haiku, só leitura), que devolve só o resumo e protege o contexto.

### 5. Verificação por hooks
A cada edição, o hook roda biome e os testes afetados. Falhou, o agente vê o erro e corrige sem você. O hook de bloqueio impede comandos perigosos.

### 6. Revisão por agente
O `revisor` (Sonnet, só leitura) compara o diff com o plano e os critérios. Uma rodada. Se o diff tocar a zona sensível, entra também a revisão de segurança.

### 7. Aprovação do merge
Você lê o diff e o relatório do revisor. Terceira reprovação seguida na revisão: pare e chame o dono.

### 8. CI
O mesmo lint, typecheck e testes, em máquina limpa. Pronto = CI verde.

## Limites

* Mesmo erro duas vezes seguidas: pare e investigue, não tente de novo no escuro.
* Estourou o orçamento da esteira: pare e decida com o dono.
* O plano cresceu para várias frentes independentes: veja a [esteira completa](completa.md).

**Próximo problema:** o trabalho tem várias frentes independentes ou risco alto. Veja a [esteira completa](completa.md).
