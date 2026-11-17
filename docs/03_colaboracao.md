<!-- Conceito: camada 3, colaboração. Cinco padrões, subagentes, quando não usar multiagente, model routing e economia de tokens -->
# Camada 3: Colaboração

> Os padrões dão a estrutura, os agentes trabalham dentro. E só divida o trabalho quando dividir se paga.

## Os cinco padrões

Antes de falar de agentes, escolha a forma do fluxo. Há cinco formas clássicas. Todos os exemplos abaixo usam o projeto de tarefas ([exemplo/](../exemplo/README.md)).

| Padrão | Ideia | Exemplo |
| --- | --- | --- |
| Encadear | Uma etapa alimenta a próxima | Plano, depois implementação, depois testes, depois revisão |
| Rotear | Uma entrada escolhe o caminho | Um pedido "corrija o typo" vai para a esteira rápida, "nova feature" para a padrão |
| Paralelizar | Subtarefas fixas, rodando juntas | Três revisões ao mesmo tempo: estilo, testes e segurança do mesmo diff |
| Orquestrar | Um coordenador decide as subtarefas na hora | Um agente lê o pedido "migrar o app para datas ISO" e descobre quais módulos mudar |
| Avaliar e otimizar | Um gera, outro critica, repete | O implementador escreve `filtrarPorData`, o revisor aponta falhas, ele corrige |

Os cinco padrões não são concorrentes. Uma esteira real usa vários: roteia o pedido pela triagem, encadeia plano e implementação, paraleliza revisões e avalia o resultado em ciclo.

Detalhando um exemplo de cada padrão com a mesma tarefa, `filtrarPorData`:

* **Encadear:** o plano define os casos, o implementador escreve os testes, depois o código, depois o revisor confere.
* **Rotear:** a triagem lê o pedido e vê que é uma função nova e pequena, então escolhe a esteira padrão em vez da completa.
* **Paralelizar:** terminado o código, rodam juntas três checagens independentes: lint, testes e revisão de segurança.
* **Orquestrar:** se o pedido fosse "adicionar datas em todo o sistema", um coordenador exploraria o código e criaria as subtarefas conforme os módulos que achasse.
* **Avaliar e otimizar:** o revisor devolve "faltou o caso de intervalo vazio", o implementador ajusta e o ciclo repete até passar, com limite de rodadas.

### Paralelizar contra orquestrar

A diferença está em quem decide as subtarefas. **No paralelo, as subtarefas são fixas e conhecidas antes.** Na revisão em três frentes, você já sabe que serão três. **No orquestrador, as subtarefas são decididas na hora**, a partir do que o coordenador descobre. Se você consegue listar as partes antes de começar, paralelize: é mais barato e previsível. Orquestre só quando a divisão depende do que se encontra pelo caminho.

Frase para guardar: os padrões dão a estrutura, os agentes trabalham dentro. Escolha o padrão primeiro, depois defina quem preenche cada caixa. Quem começa pelos agentes costuma terminar com um desenho cheio de caixas que não fazem diferença.

## Subagentes

Um subagente é um agente que o principal chama para uma tarefa específica. Ele começa com contexto limpo: não herda a conversa do pai nem as skills dele, e devolve só um resumo. Isso traz dois ganhos:

* **Especialização:** cada um tem seu prompt, suas ferramentas e seu modelo. O revisor só lê, o implementador edita.
* **Higiene de contexto:** o explorador pode abrir trinta arquivos para responder "onde fica o filtro de status?" e devolver três linhas. O contexto do principal fica limpo.

Subagentes vivem em `.claude/agents/*.md`, com frontmatter como `name`, `description`, `tools` e `model`. Neste repositório os três são só leitura.

Um exemplo de especialização na prática:

1. O principal recebe "ache onde as tarefas são ordenadas".
2. Chama o explorador, que roda em haiku e só lê.
3. O explorador abre quinze arquivos e devolve "ordenação em `src/listar.ts`, linha 12".
4. O principal segue com o contexto limpo, sem os quinze arquivos.

Um detalhe importante: o subagente não herda as skills do pai. Se ele precisar de uma, liste no campo `skills` do frontmatter para pré-carregar. Campos como `disallowedTools` e `permissionMode` reforçam o limite do que ele pode fazer, e `isolation: worktree` o coloca numa cópia separada do repositório.

## Quando NÃO usar multiagente

Multiagente é caro e frágil. Evite quando:

* **As tarefas são acopladas.** Se a mudança em `tarefas.ts` afeta `listar.ts` e o teste ao mesmo tempo, dois agentes editando em paralelo vão se atropelar.
* **O contexto é compartilhado.** Se todos precisam saber tudo o que os outros decidiram, você gasta a economia de contexto em reunião entre agentes.
* **O custo de tokens é várias vezes maior.** Cada agente carrega o próprio contexto, e a coordenação também consome tokens. Para uma tarefa de uma hora, o dobro ou o triplo de gasto raramente se paga.

Teste de bolso: um único agente com bom plano resolve? Então use um só.

Sinais de que você está usando agentes demais:

* O resumo do subagente é quase do tamanho do que ele leu.
* Dois agentes editam o mesmo arquivo e um desfaz o outro.
* O tempo total ficou maior que o de um agente só.
* Você não consegue explicar em uma frase o que cada agente adiciona.

Se algum desses aparecer, junte os papéis. Voltar a um agente só não é retrocesso: é ajuste de processo.

## Model routing: o menor modelo que passa no teste

Nem todo papel precisa do modelo mais forte. A regra: **o menor modelo que passa no teste.** Comece pelo menor, meça e suba só se falhar.

| Subagente | Modelo | Papel | Por que esse modelo |
| --- | --- | --- | --- |
| explorador | haiku | Busca e lê arquivos, devolve achados | Tarefa mecânica, volume alto, precisa ser barata e rápida |
| revisor | sonnet | Revisa o diff contra o plano e os critérios | Exige julgamento, mas não o mais caro |
| seguranca | opus | Audita risco alto: auth, segredos, permissões | Um erro aqui custa mais que o modelo |

O campo `model` do frontmatter aceita `haiku`, `sonnet`, `opus` ou `inherit`.

Como aplicar o roteamento sem adivinhar: comece com o menor modelo, rode o seu teste de aceite e, se falhar, suba um degrau registrando o motivo. Com o tempo você tem uma tabela baseada em dados, e não em medo.

## Economia de tokens

Quatro hábitos que reduzem custo sem perder qualidade:

* **Cache:** manter o início do prompt estável (CLAUDE.md curto e fixo) permite reaproveitar o cache entre chamadas.
* **Skills sob demanda:** o roteiro longo só entra quando a tarefa pede.
* **Custo do multiagente:** conte os agentes antes de criá-los. Cada um é um contexto a mais para pagar.
* **Plano antes do código:** errar no plano custa uma frase. Errar no código custa uma refatoração e uma rodada de testes.

Em números, o raciocínio é simples. Se um agente gasta 100 mil tokens, três agentes que não compartilham o contexto podem gastar 300 mil ou mais, mais a coordenação. A divisão só compensa se economizar tempo de uma pessoa ou melhorar o resultado de forma que você consiga medir.

## Onde ver no repositório

* Subagentes com modelo e ferramentas: [explorador](../.claude/agents/explorador.md), [revisor](../.claude/agents/revisor.md) e [seguranca](../.claude/agents/seguranca.md)
* Roteador dos padrões: [triagem](../.claude/skills/triagem/SKILL.md)
* Encadear, rotear e avaliar na prática: [esteira padrão](../esteiras/padrao.md)
* Orquestrar com ondas e paralelo: [esteira completa](../esteiras/completa.md)
* O caso mais simples, sem subagente: [esteira rápida](../esteiras/rapida.md)
* Medir o custo do multiagente: [observabilidade/README.md](../observabilidade/README.md)

## Regra de decisão em uma linha

Comece com um agente e um bom plano. Adicione um subagente quando houver um motivo claro: isolar contexto, restringir ferramentas ou usar um modelo mais barato. Adicione paralelismo quando as partes forem independentes. Adicione um orquestrador só quando a divisão do trabalho depender do que for descoberto. Em todo degrau, meça se valeu a pena.

Exemplo de decisão no projeto de tarefas:

* Corrigir um typo em `tarefas.ts`: um agente, esteira rápida, sem subagente.
* Implementar `filtrarPorData`: um implementador e um explorador, esteira padrão.
* Trocar o armazenamento em memória por banco, tocando vários módulos e a segurança: aí uma orquestração pode se pagar.

Perceba que o tamanho do problema, e não a vontade de usar a ferramenta nova, escolhe o desenho.

Perguntas para fazer antes de criar um subagente novo:

* Que contexto ele evita de poluir?
* Que ferramenta ele não deve ter?
* Que modelo mais barato dá conta?
* Como vou saber se ele ajudou?

## Teste seu entendimento

1. Você quer rodar lint, testes e revisão de segurança sobre o mesmo diff ao mesmo tempo. É paralelizar ou orquestrar? Por quê?
2. Dê um exemplo de tarefa no projeto de tarefas em que usar três agentes seria pior que usar um.
3. Por que o explorador roda em haiku e a segurança em opus? O que mudaria se você trocasse os dois?

**Próximo problema:** mais agentes significam mais risco. Como impedir, medir e corrigir os erros? Veja [04_producao.md](04_producao.md).
