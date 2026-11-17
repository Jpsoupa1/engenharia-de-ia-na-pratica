<!-- Conceito: camada 5, prática. Vault com Claude Code, esteira padrão em oito passos e processo proporcional à tarefa -->
# Camada 5: Prática

> O modelo não tem estado, mas o vault tem. E o processo certo é o mais leve que resolve a tarefa.

## Obsidian com Claude Code

O vault é uma pasta de notas em markdown. Como é só arquivo, o Claude Code lê e escreve nele sem integração especial. É a memória episódica e procedural da camada 2 posta em prática: decisões, planos e lições que sobrevivem à sessão.

A estrutura mínima está em [vault_exemplo/](../vault_exemplo/CLAUDE.md):

* `projetos/<nome>/indice.md`: o resumo do projeto e os links para o que importa.
* `decisoes/`: o porquê das escolhas, uma nota por decisão.
* `sessoes/`: o que foi feito em cada sessão.
* `templates/`: modelos de plano, decisão e sessão.

Exemplo: terminou a feature de filtro por data. O agente grava uma nota de sessão e, se houve escolha difícil (comparar datas como texto ISO em vez de converter para `Date`), uma nota de decisão. Amanhã, outra sessão começa lendo o índice e sabe de tudo isso. O modelo não lembrou: o vault lembrou.

Dois cuidados: o índice deve dizer quais notas abrir para cada tipo de tarefa, para o agente não ler o vault inteiro, e **nunca grave segredo no vault.**

Quando o vault vale a pena? Quando você trabalha em um projeto por semanas e a mesma explicação se repete a cada sessão. Para um script descartável, ele é peso morto.

Um índice enxuto do projeto de exemplo tem o seguinte formato:

* Resumo em três linhas do que o projeto faz.
* Comandos que importam: `npm test`, `npm run lint`, `npm run typecheck`.
* Armadilhas conhecidas, por exemplo "datas são texto ISO, não `Date`".
* Links para as decisões e sessões mais relevantes.

Um índice assim custa poucas linhas de contexto e economiza dezenas de perguntas.

## A esteira padrão em oito passos

A esteira padrão serve para uma tarefa de uma a três horas com alguma investigação. Ela encadeia tudo o que as camadas anteriores ensinaram:

| Passo | O que acontece | Conceito |
| --- | --- | --- |
| 1 Contexto | Lê o índice do projeto e só as notas ligadas à tarefa | Selecionar, memória episódica |
| 2 Plano | Escreve um plano enxuto com critérios de aceite antes do código | Plano antes do código |
| 3 Aprovação do plano | Você lê e diz sim ou ajusta | Portão humano, autonomia nível 3 |
| 4 Implementação | Um implementador escreve o código, com o subagente explorador para buscas | Subagentes, isolar contexto, model routing |
| 5 Verificação por hooks | Biome e vitest rodam a cada edição, sem pedir | Guardrail determinístico, verificação |
| 6 Revisão por agente | O revisor compara o diff com o plano e os critérios | Avaliar e otimizar |
| 7 Aprovação do merge | Você vê o resumo e aprova | Portão humano |
| 8 CI | O CI roda tudo de novo na integração | Verificação independente do agente |

Na prática, com o projeto de exemplo, o pedido é: implementar `filtrarPorData(tarefas, { de?, ate? })`. O plano lista os casos (só `de`, só `ate`, os dois, nenhum, intervalo vazio). Os testes nascem desses casos. O pedido é pequeno o bastante para um único implementador, e por isso não precisa de orquestração.

Para escolher a esteira, comece sempre pela [triagem](../.claude/skills/triagem/SKILL.md): ela mede tamanho, incerteza e risco e escolhe a esteira mais leve que resolve.

Detalhando os pontos que mais confundem:

* **Passo 1 contra 2:** ler o contexto não é ler o repositório inteiro. É ler o índice e as duas ou três notas ligadas à tarefa.
* **Passo 3:** a aprovação do plano é o portão mais barato do processo. Um erro de entendimento aqui custa uma frase para corrigir.
* **Passo 5:** a verificação por hooks é automática e silenciosa quando passa. Você só vê quando falha, e o agente corrige antes de seguir.
* **Passo 6:** o revisor tem contexto limpo e só lê. Por isso enxerga o que o implementador, preso à própria ideia, deixou passar.
* **Passo 8:** o CI não confia no agente nem no hook. Roda de novo, do zero, em outra máquina.

Quando a tarefa é pequena, corte passos em vez de fazê-los pela metade. A esteira rápida existe para isso. Quando o risco é alto, acrescente auditoria de segurança. O desenho é uma régua, não um ritual.

## Processo proporcional à tarefa

Uma história real, sem nomes. Uma equipe adotou um processo completo: plano, revisão, auditoria, registro, tudo em toda tarefa. Uma tarefa de cerca de 3 horas passou a levar cerca de 15. Ninguém percebeu na hora, porque cada etapa parecia razoável sozinha.

O que mudou o jogo foi medir. A telemetria mostrou onde o tempo ia: esperas, revisões duplicadas e auditoria em mudança trivial. A correção foi criar esteiras de pesos diferentes, uma para cada tamanho de tarefa. Hoje o mesmo trabalho de 3 horas volta a levar perto de 3.

A lição: o padrão é o mais simples que resolve, orquestração só entra quando se paga, e para saber, meça. Rode `python3 observabilidade/relatorio.py` sobre a sua `.telemetria/` e veja a duração, as chamadas de ferramenta e os subagentes de cada sessão.

O que medir para saber se o seu processo está no peso certo:

* Tempo total da tarefa, do pedido ao merge.
* Número de rodadas de revisão. Mais de duas indica plano fraco ou critério vago.
* Quantas vezes o mesmo erro voltou. Se voltou, falta uma catraca.
* Quantos tokens e subagentes a tarefa consumiu.

Se o tempo cresce sem que a qualidade melhore, tire uma etapa. Se a qualidade cai, acrescente uma. A decisão é sempre baseada no que você mediu.

## Como começar amanhã

Três passos, nesta ordem, sem instalar nada além do Claude Code:

1. **Escreva um CLAUDE.md curto**, com menos de 60 linhas: comandos de teste e lint, convenções que o agente erra, e o que nunca fazer. Só o que vale para toda tarefa. Se o seu está inchado, use o [exercício](../exercicios/claude_md_inchado.md).
2. **Peça o plano antes do código.** Em qualquer tarefa que toque mais de um arquivo, diga "escreva o plano e espere meu sim". É a mudança de menor custo e maior retorno.
3. **Transforme o primeiro erro repetido em hook ou teste.** Quando o agente errar a mesma coisa pela segunda vez, não repita a instrução: aplique a regra da catraca.

Depois, escolha entre a [esteira rápida, padrão ou completa](../esteiras/README.md) pela tarefa, não pelo costume, e comece pelas mais leves.

## Onde ver no repositório

* Esteiras: [README](../esteiras/README.md), [rapida](../esteiras/rapida.md), [padrao](../esteiras/padrao.md) e [completa](../esteiras/completa.md)
* Planejamento: [planejar](../.claude/skills/planejar/SKILL.md) e [exemplo de plano](../.claude/skills/planejar/exemplos/feature_filtro_data.md)
* Revisão e registro: [revisar](../.claude/skills/revisar/SKILL.md), [registrar-lição](../.claude/skills/registrar-licao/SKILL.md) e [handoff](../.claude/skills/handoff/SKILL.md)
* Vault: [CLAUDE.md do vault](../vault_exemplo/CLAUDE.md), [índice](../vault_exemplo/projetos/exemplo/indice.md) e [templates](../vault_exemplo/templates/plano.md)
* CI: [.github/workflows/ci.yml](../.github/workflows/ci.yml)
* Medição: [observabilidade/README.md](../observabilidade/README.md)
* Projeto da feature: [exemplo/README.md](../exemplo/README.md)

## Erros comuns

* Usar a esteira completa por hábito, em tarefa de dez minutos.
* Pular a aprovação do plano porque "é rápido".
* Gravar no vault tudo o que acontece, até ele virar ruído.
* Nunca olhar a telemetria depois de ligá-la.

## Resumo das três esteiras

* **Rápida:** o agente principal sozinho, para tarefa pequena de baixo risco. Sem plano formal e sem subagente.
* **Padrão:** plano aprovado, um implementador, uma revisão e CI. É a escolha para a maioria das tarefas de uma a três horas.
* **Completa:** várias frentes independentes ou risco alto, com ondas de implementadores em paralelo e auditoria.

Na dúvida, comece pela mais leve. Subir de esteira exige uma justificativa escrita, e isso já filtra a maior parte dos excessos.

Uma última dica de adoção: faça a primeira semana com a esteira mais leve e anote o que incomodou. Esse registro vira a lista do que automatizar com um hook ou uma skill.

## Teste seu entendimento

1. Em quais dois passos da esteira padrão você, e não o agente, decide? Por que eles estão nesses pontos?
2. Por que medir foi a correção do caso das 15 horas, e não "pedir ao agente para ser mais rápido"?
3. Escolha uma tarefa sua de hoje e diga qual esteira você usaria e qual passo você cortaria.

**Próximo problema:** escolher a esteira certa para cada tarefa e colocá-la em prática. Veja [esteiras/README.md](../esteiras/README.md).
