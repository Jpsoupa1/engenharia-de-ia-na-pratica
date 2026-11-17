<!-- Conceito: respostas diretas às dúvidas mais comuns de quem vai começar a usar um agente de código. -->
# Perguntas frequentes

## A IA inventa código. Como confiar?

Não confie, verifique. O agente erra, e a engenharia em volta existe por isso. Três defesas:

* Testes, lint e typecheck rodando a cada edição, via hook. O erro volta para o agente na hora.
* Revisão por um agente separado, com contexto limpo, que só lê.
* Você lê o diff antes do merge, e o CI roda de novo.

Um erro que se repete vira regra, teste ou hook (regra da catraca). Veja [fundação](01_fundacao.md) e [produção](04_producao.md).

## Isso vai substituir devs?

O que a aula mostra é outra coisa: o trabalho muda de lugar. Sai um pouco de digitar código, entra mais definir critérios de aceite, desenhar o processo, revisar e medir. Quem sabe especificar e verificar ganha alavancagem. Ninguém aqui afirma o que acontece com o mercado. O que dá para afirmar é que o agente sem critério claro e sem revisão produz retrabalho.

## E os dados sigilosos?

Confira a política de dados do plano que você contratou, antes de colocar código ou dados de cliente na ferramenta. Ela diz o que é retido, por quanto tempo e se entra em treinamento. Não assuma, leia. Além disso:

* Segredo nunca entra no contexto nem no repositório. Veja [seguranca/checklist.md](../seguranca/checklist.md).
* Bloqueie a leitura de `.env` e chaves por permissão e por hook.
* Use sandbox para limitar rede e escrita.

## Qual a diferença para o Copilot?

É diferença de modo de uso. O assistente de editor completa código e responde no chat, com você dirigindo cada passo. O agente no terminal recebe um objetivo e executa ferramentas em loop: lê arquivos, edita, roda testes, vê o erro e tenta de novo. Hoje há sobreposição entre as categorias, então compare pelo fluxo de trabalho que você quer: sugestão linha a linha ou tarefa delegada com revisão no fim.

## Quanto custa?

Custa tokens, e o custo cresce com contexto grande, muitos subagentes e modelo maior do que o necessário. O que reduz:

* Plano antes do código, para não refazer.
* Model routing: o menor modelo que passa no teste.
* Skills sob demanda e CLAUDE.md curto, para não gastar contexto à toa.
* Prompt caching e esteira proporcional: tarefa pequena não precisa de multiagente.

Para saber o custo real, meça. Veja [observabilidade](../observabilidade/README.md). Consulte os preços atuais na página do fornecedor.

## E a dependência de fornecedor?

Dá para reduzir:

* `AGENTS.md` é um formato aberto de instruções para agentes. O `CLAUDE.md` deste repositório começa importando o `AGENTS.md`.
* MCP é um padrão aberto: o mesmo servidor serve a mais de um cliente.
* Skills são markdown em pasta. Você leva os arquivos para onde quiser.
* Testes, CI e ADRs ficam no seu repositório, não na ferramenta.

Parte do comportamento ainda é específica da ferramenta (hooks, formato de subagente), então isole isso em poucos arquivos.

## Como revisar código que eu não escrevi?

Do mesmo jeito que revisa o de um colega, com mais atenção ao que testa:

* Leia o plano aprovado e confira se o diff cumpre os critérios de aceite.
* Veja os testes: cobrem o caso negado, não só o permitido?
* Procure o que não foi pedido: arquivos tocados à toa, dependência nova, config alterada.
* Rode o código. Não confie só no "testes passam".
* Peça ao agente revisor um relatório e use-o como segunda opinião, não como substituto.

Veja a skill [revisar](../.claude/skills/revisar/SKILL.md).

## E os juniores?

O risco é aceitar sem entender. O que ajuda:

* Pedir que o agente explique o diff e o porquê das escolhas.
* Fazer o júnior escrever os critérios de aceite antes do código.
* Revisão humana obrigatória nos portões.
* Registrar lições (skill registrar-licao), para o aprendizado ficar no repositório.

Júnior que usa o agente como tutor aprende mais rápido. Júnior que só copia não aprende.

## Por onde começar?

Amanhã, faça duas coisas:

1. Escreva um `CLAUDE.md` curto, com menos de 60 linhas: comandos de teste, convenções que o código não mostra, o que nunca fazer.
2. Peça um plano antes do código e aprove o plano.

Depois siga os [exercícios](../exercicios/README.md), um por camada.
