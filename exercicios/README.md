<!-- Conceito: cinco exercícios práticos, um por camada da aula, para aplicar cada ideia no projeto exemplo/. -->
# Exercícios

Cinco exercícios, um por camada. Faça na ordem. Cada um diz como saber que deu certo.

Pré-requisito: Node instalado e `npm install` feito dentro de `exemplo/`.

## Exercício 1: fundação, ver o loop do agente

**Objetivo:** enxergar que o agente é modelo mais harness, rodando em loop.

**Passos:**
1. Abra o Claude Code na raiz do repositório.
2. Peça: "Liste as funções exportadas em `exemplo/src/listar.ts` e rode os testes do projeto."
3. Observe cada passo: o agente pensa, chama uma ferramenta (buscar, ler, rodar) e observa o resultado.
4. Anote quais ferramentas foram usadas e em que ordem.

**Como saber que deu certo:** você consegue apontar, na saída, o objetivo, o pensar, o agir e o observar, e dizer qual parte é o modelo e qual é o harness (a execução do teste, por exemplo).

## Exercício 2: conhecimento, enxugar um CLAUDE.md

**Objetivo:** aplicar as alavancas de contexto: selecionar e persistir só o que vale.

**Passos:**
1. Leia [claude_md_inchado.md](claude_md_inchado.md). Ele é ruim de propósito.
2. Marque cada trecho com uma destas etiquetas: repete o código, vago, histórico velho, contraditório, deveria ser skill, deveria ser hook.
3. Escreva uma versão com menos de 60 linhas, só com o que o agente não descobre sozinho.
4. Mova o procedimento longo para uma skill e a regra obrigatória para um hook (descreva onde cada um ficaria, não precisa escrever).

**Como saber que deu certo:** a nova versão tem menos de 60 linhas, nenhuma regra vaga e nenhuma contradição, e cada coisa removida tem destino (código, skill, hook ou lixo).

## Exercício 3: colaboração, um subagente que só lê

**Objetivo:** ver o isolamento de contexto de um subagente.

**Passos:**
1. Peça: "Use o agente explorador para descobrir onde `filtrarPorStatus` é usado e me diga em uma frase."
2. Observe que a resposta volta como resumo, sem as leituras de arquivo no seu contexto.
3. Abra [explorador.md](../.claude/agents/explorador.md) e confira o `model` e as `tools`.
4. Tente pedir ao explorador que edite um arquivo e veja a recusa.

**Como saber que deu certo:** você recebeu um resumo curto, o explorador não conseguiu editar, e você sabe dizer por que Haiku e só leitura bastam para essa tarefa.

## Exercício 4: produção, um hook que corrige o agente

**Objetivo:** ver um guardrail determinístico e a regra da catraca.

**Passos:**
1. Em `exemplo/src/listar.ts`, quebre de propósito o filtro. Por exemplo, em `filtrarPorStatus`, troque `===` por `!==`.
2. Peça ao agente: "Faça uma pequena melhoria de legibilidade em `listar.ts`."
3. Ao editar o arquivo, o hook [lint_e_testes.py](../.claude/hooks/lint_e_testes.py) roda biome e `vitest related`. O teste falha, o hook sai com código 2 e devolve o erro no stderr.
4. Veja o agente ler o erro e corrigir sozinho.
5. Agora chame a skill [registrar-licao](../.claude/skills/registrar-licao/SKILL.md) e registre a lição: "mudar operador de comparação sem rodar teste quebra o filtro". Decida se vira regra, teste ou hook.

**Como saber que deu certo:** você viu o erro do teste voltar ao agente sem você copiar nada, o agente consertou, e a lição ficou registrada com o destino (regra, teste ou hook).

## Exercício 5: prática, a esteira padrão e a medida

**Objetivo:** percorrer a [esteira padrão](../esteiras/padrao.md) e medir.

**Passos:**
1. Peça a feature: "Implemente `filtrarPorData(tarefas, { de?, ate? })` em `exemplo/src/listar.ts`." Deixe a triagem escolher a esteira. Se ela escolher a padrão, siga.
2. Leia e aprove o plano, conferindo os critérios do [caso 1](../evals/casos.md).
3. Deixe o agente implementar, os hooks verificarem e o revisor revisar.
4. Leia o diff e confirme `npm test`, `npm run lint` e `npm run typecheck` dentro de `exemplo/`.
5. Rode o relatório:
   ```bash
   python3 observabilidade/relatorio.py .telemetria/
   ```
6. Preencha a tabela do caso 1: data, esteira, modelo, tempo de relógio e tempo humano.

**Como saber que deu certo:** os testes novos passam, incluindo o intervalo vazio, o relatório mostra a sessão com duração e chamadas de ferramenta, e a tabela tem uma linha preenchida. Compare o tempo de relógio com o tempo humano: o segundo deve ser bem menor.

**Próximo problema:** guardar o que aprendeu entre sessões. Veja o [vault de exemplo](../vault_exemplo/CLAUDE.md).
