<!-- Conceito: camada 4, produção. Harness engineering, guardrails, catraca, autonomia, evals, tríade letal e escala -->
# Camada 4: Produção

> Harness engineering é projetar o que o sistema deve impedir, medir e corrigir.

## Harness engineering e os cinco componentes

Em produção, a pergunta muda. Deixa de ser "o agente consegue?" e vira "o que acontece quando ele erra?". Harness engineering é a resposta: desenhar o entorno para que erros sejam barrados, vistos e consertados. O harness tem cinco componentes:

| Componente | O que faz | Onde ver |
| --- | --- | --- |
| Contexto | Entrega as regras e o conhecimento certos | [CLAUDE.md](../CLAUDE.md), [skills](../.claude/skills/triagem/SKILL.md) |
| Ferramentas | Define o que o agente pode fazer | [settings.json](../.claude/settings.json), [subagentes](../.claude/agents/explorador.md) |
| Guardrails | Impede ações e saídas perigosas | [bloquear_perigosos.py](../.claude/hooks/bloquear_perigosos.py) |
| Verificação | Confere o resultado antes de aceitar | [lint_e_testes.py](../.claude/hooks/lint_e_testes.py), [evals](../evals/README.md) |
| Observabilidade | Registra o que aconteceu para medir | [telemetria.py](../.claude/hooks/telemetria.py), [relatorio.py](../observabilidade/relatorio.py) |

Um modo útil de olhar: cada componente responde a uma pergunta.

* Contexto: o agente sabe o que precisa saber?
* Ferramentas: ele só pode o que deveria poder?
* Guardrails: o que acontece se ele tentar algo perigoso?
* Verificação: como sei que o resultado está certo?
* Observabilidade: como descubro, depois, o que ele fez e quanto custou?

Se você não sabe responder uma delas para o seu projeto, esse é o buraco do seu harness.

## Guardrails: entrada, ação e saída

Guardrail é uma barreira em um ponto do fluxo. Há três pontos e dois jeitos de construir cada um:

| Ponto | Determinístico | Baseado em modelo |
| --- | --- | --- |
| Entrada | Regex que recusa pedido com chave de API colada | Classificador que detecta pedido malicioso |
| Ação | Hook que nega `git push --force` | Revisor que avalia se a ação faz sentido |
| Saída | Teste que falha se o filtro devolver tarefa fora do período | Juiz que avalia a resposta contra uma rubrica |

Determinístico é regra de código: sempre dá a mesma resposta, é barato e auditável, mas só pega o que você previu. Baseado em modelo entende contexto e pega o imprevisto, mas pode errar e custa tokens. Regra prática: use o determinístico para tudo que dá para escrever como regra, e o modelo para o resto.

## Hooks contra instrução no prompt

Escrever "nunca leia o .env" no CLAUDE.md é um pedido, e o modelo pode ignorá-lo, esquecê-lo ou ser enganado. Um hook é uma garantia: o harness executa o seu script antes ou depois da ferramenta, e o modelo não decide se ele roda.

Como funciona: o hook recebe um JSON no stdin (`session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input` e outros). Saída com código 0 deixa passar. Código 2 bloqueia no PreToolUse, ou devolve o stderr ao agente no PostToolUse. Qualquer outro código é erro que não bloqueia. Um hook de PreToolUse também pode responder JSON com `permissionDecision: "deny"` e um `permissionDecisionReason`, que o agente lê e usa para tentar outro caminho. Hooks rodam também nas ferramentas chamadas por subagentes.

Eventos disponíveis incluem SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, SubagentStart, SubagentStop, Stop, PreCompact, PostCompact, SessionEnd e Notification.

Exemplo de hook de ação que bloqueia: o agente tenta `rm -rf ../` para limpar uma pasta. O `bloquear_perigosos.py` responde `deny` com o motivo "remoção recursiva fora do projeto". O agente lê o motivo, desiste desse comando e usa outro caminho dentro do projeto. Ninguém precisou intervir, e o erro ficou registrado na telemetria.

## A regra da catraca

Catraca só gira para um lado. A regra: **erro que se repete vira regra, teste ou hook, e não volta.** O agente apagou um arquivo fora do projeto? Isso vira uma entrada no `bloquear_perigosos.py` com um teste em [test_hooks.py](../.claude/hooks/test_hooks.py). Esqueceu de rodar o lint? Vira o hook `lint_e_testes.py`. A lição vira estrutura, não só uma anotação que alguém precisa lembrar de ler. A skill [registrar-licao](../.claude/skills/registrar-licao/SKILL.md) conduz esse registro.

## Quatro níveis de autonomia

Autonomia não é liga e desliga. São quatro níveis, e cada nível tem seus portões, que são os pontos onde um humano decide.

| Nível | Comportamento | Portões |
| --- | --- | --- |
| 1 Sugere | O agente propõe, você executa | Você aplica cada mudança |
| 2 Age com aprovação a cada passo | Cada edição e comando pede um sim | Todo passo |
| 3 Age e o humano revisa nos portões | Trabalha sozinho entre pontos fixos | Aprovação do plano, aprovação do merge |
| 4 Autônomo | Executa de ponta a ponta | Só os guardrails e o CI |

A esteira padrão deste repositório opera no nível 3: o agente trabalha sozinho entre dois portões, o do plano e o do merge. Suba de nível só para tarefas de baixo risco e com verificação forte.

Aplicar a autonomia por tipo de tarefa, e não por pessoa ou por humor:

* Renomear uma variável com testes cobrindo: nível 3 ou até 4.
* Mudar uma regra de permissão: nível 2, com sua leitura em cada passo.
* Tocar em autenticação ou dados pessoais: nível 3 com auditoria e portão extra.

## Evals e LLMOps

Eval é teste para comportamento de IA. Você define casos de entrada, o resultado esperado e uma rubrica, e roda sempre que mudar prompt, modelo ou skill. Sem eval, "melhorei o prompt" é opinião. LLMOps é o conjunto de práticas para operar isso: versionar prompts, rodar evals no CI, acompanhar custo e latência, ler a telemetria. A rubrica de um juiz baseado em modelo vive em [rubrica_juiz.md](../evals/rubrica_juiz.md).

## Tríade letal e sandbox

A combinação perigosa tem três ingredientes juntos: **dados privados, conteúdo não confiável e um canal de saída.** Se o agente lê seu `.env` (privado), abre uma página com uma instrução escondida (não confiável) e pode fazer uma requisição web (saída), alguém pode roubar o segredo. A defesa é quebrar a tríade: tire ao menos um dos três.

A permissão `deny` em Read bloqueia a ferramenta de leitura, mas não cobre um subprocesso que abra o arquivo sozinho. Para isso existe o sandbox (`/sandbox`): limites do sistema operacional no shell, com escrita só no diretório de trabalho e rede por proxy com uma lista de domínios que começa vazia. Vem desligado por padrão.

Um bom eval começa pequeno: cinco a dez casos reais, incluindo ao menos um caso que o agente deve recusar. Cresce quando um erro novo aparece, pela mesma lógica da catraca.

## Escala em quatro níveis

| Nível | O que usa |
| --- | --- |
| Você | CLAUDE.md pessoal em `~/.claude/` |
| Projeto | CLAUDE.md e `.claude/` do repositório, versionados |
| Time | Plugin instalado por marketplace, com skills, agentes e hooks |
| Organização | Política gerenciada, que vence as configurações de baixo |

O plugin deste repositório mostra o nível do time: veja [plugin/README.md](../plugin/README.md). Instalação: `/plugin marketplace add <dono>/engenharia-de-ia-na-pratica` e depois `/plugin install ia-na-pratica@engenharia-de-ia-na-pratica`. Para testar localmente, `claude --plugin-dir .`. Um projeto pode declarar `extraKnownMarketplaces` e `enabledPlugins` no settings.json.

Quando duas skills têm o mesmo nome, a da empresa vence a pessoal, e a pessoal vence a do projeto. Skills de plugin usam o prefixo `plugin:skill` e por isso não colidem com as suas.

## O settings.json, bloco a bloco

O `settings.json` é JSON puro e **não aceita comentário**. Por isso a explicação fica aqui, e não dentro do arquivo. As permissões são avaliadas na ordem deny, depois ask, depois allow, e a primeira regra que casa decide.

* **`permissions.allow`:** leitura e testes (por exemplo `Bash(npm test *)`) rodam sem perguntar. Demonstra o menor atrito para o que é seguro e previsível, e o nível 3 de autonomia.
* **`permissions.ask`:** `git push` e edição de arquivos de configuração pedem confirmação. Demonstra os portões humanos: ações com efeito fora da máquina ou que mudam o próprio harness passam por você.
* **`permissions.deny`:** `Read(./.env)` e leitura de chaves ficam proibidas. Demonstra negar por padrão e quebrar a tríade letal. Lembre do limite: não cobre subprocesso, daí o sandbox.
* **`hooks`:** liga os scripts em `.claude/hooks/` aos eventos. O `bloquear_perigosos.py` entra em PreToolUse com matcher `Bash`. O `lint_e_testes.py` entra em PostToolUse com matcher `Edit|Write`. O `telemetria.py` entra nos eventos de sessão, ferramenta e subagente e grava JSONL em `.telemetria/`. Demonstra guardrail determinístico, verificação e observabilidade. Os caminhos usam `${CLAUDE_PROJECT_DIR}`.

Um exemplo de ciclo: o agente edita `exemplo/src/listar.ts`, o hook roda o biome e o `vitest related`. Se falhar, sai com código 2, o agente lê o erro e corrige no mesmo loop. Depois, `python3 observabilidade/relatorio.py` mostra a duração, as chamadas e os subagentes da sessão.

## Onde ver no repositório

* Permissões e hooks: [.claude/settings.json](../.claude/settings.json)
* Guardrail de ação: [bloquear_perigosos.py](../.claude/hooks/bloquear_perigosos.py)
* Verificação: [lint_e_testes.py](../.claude/hooks/lint_e_testes.py) e os testes dos hooks em [test_hooks.py](../.claude/hooks/test_hooks.py)
* Observabilidade: [telemetria.py](../.claude/hooks/telemetria.py), [relatorio.py](../observabilidade/relatorio.py) e [exemplo.jsonl](../observabilidade/exemplo.jsonl)
* Evals: [evals/README.md](../evals/README.md), [casos.md](../evals/casos.md) e [rubrica_juiz.md](../evals/rubrica_juiz.md)
* Segurança: [seguranca/checklist.md](../seguranca/checklist.md)
* Escala: [plugin/hooks.json](../plugin/hooks.json) e [.claude-plugin/plugin.json](../.claude-plugin/plugin.json)

## Teste seu entendimento

1. Por que um hook que nega `git push --force` é mais confiável que a mesma regra escrita no CLAUDE.md?
2. Em qual nível de autonomia está a esteira padrão e quais são os seus dois portões?
3. Um agente lê issues de terceiros, tem acesso ao banco de produção e pode chamar uma URL externa. Que parte da tríade letal você tiraria primeiro, e como?

**Próximo problema:** com as proteções no lugar, como usar tudo isso num dia comum sem virar burocracia? Veja [05_pratica.md](05_pratica.md).
