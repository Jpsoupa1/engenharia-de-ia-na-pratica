<!-- Conceito: vocabulário da aula em ordem alfabética, para consulta rápida. -->
# Glossário

Termos da aula, em ordem alfabética. Cada um tem uma ou duas linhas.

**ADR.** Registro de decisão de arquitetura: contexto, alternativas, decisão e consequências, em uma página curta. Explica por que o código é assim.

**Agente.** Modelo mais harness, rodando em loop: recebe um objetivo, pensa, age com ferramentas, observa o resultado e repete até terminar.

**Alavancas (do contexto).** As quatro formas de combater o context rot: selecionar o que entra, comprimir o que já está, isolar em outro contexto e persistir fora da conversa.

**Busca agêntica.** O agente procura sozinho com grep, glob e leitura de arquivos, em vez de consultar um índice vetorial. É o que o Claude Code faz no código.

**Catraca (regra da).** Erro que se repete vira regra, teste ou hook, e não volta mais. O processo só anda para a frente.

**Context rot.** Perda de qualidade conforme o contexto enche. Quanto mais coisa na janela, pior o modelo acha o que importa.

**Contextual Retrieval.** Técnica de RAG em que cada trecho indexado ganha, antes, uma frase de contexto sobre de onde veio. Melhora o que a busca encontra.

**Divulgação progressiva.** O agente vê só o nome e a descrição das skills na abertura. O corpo carrega quando a skill é usada, e os arquivos de apoio só quando o corpo manda ler.

**Esteira.** Fluxo de trabalho com etapas e portões. Aqui são três: rápida, padrão e completa, escolhidas conforme o tamanho da tarefa.

**Eval.** Teste de qualidade do agente: casos reais, rodados, pontuados e comparados ao longo do tempo. Responde "ficou melhor ou pior?".

**Fine tuning.** Treinar o modelo com exemplos para mudar como ele se comporta. Caro e lento. Vem depois de contexto e RAG.

**Guardrail.** Limite que impede, mede ou corrige o comportamento do agente. Pode agir na entrada, na ação ou na saída. Determinístico (código) ou baseado em modelo.

**Handoff.** Passagem de bastão entre sessões: objetivo, decisões, estado, próximos passos e lições, gravados para a próxima sessão começar de onde parou.

**Harness.** Tudo em volta do modelo que o transforma em agente: loop, ferramentas, contexto, permissões, hooks. Agente = modelo + harness.

**Hook.** Script que o Claude Code roda em um evento (antes de uma ferramenta, depois dela, ao parar). Executa sempre, diferente de uma instrução no prompt.

**LLM como juiz.** Usar um modelo para pontuar a saída de outro, seguindo uma rubrica. Escala melhor que revisão humana, mas precisa de calibração.

**LLMOps.** Operar sistemas com LLM em produção: versionar prompts, rodar evals, observar custo e qualidade, corrigir regressões.

**Marketplace.** Catálogo de plugins que um time adiciona ao Claude Code. Aqui: `engenharia-de-ia-na-pratica`.

**MCP (Model Context Protocol).** Padrão aberto para ligar o agente a sistemas externos. Um servidor MCP oferece ferramentas, recursos e prompts. Custa contexto e traz risco de segurança.

**Memória de trabalho.** O que está na janela de contexto agora. Some quando a sessão acaba.

**Memória episódica.** O que aconteceu: sessões passadas, decisões, erros. No exemplo, as notas de sessão do vault.

**Memória procedural.** Como fazer: skills, regras e hooks. Instruções que viram hábito.

**Memória semântica.** Fatos estáveis sobre o projeto: arquitetura, convenções, glossário. Memória velha é pior que nenhuma, então precisa de manutenção.

**Menor privilégio.** O agente recebe só as permissões de que precisa para a tarefa. Um revisor só lê, então só tem ferramentas de leitura.

**Model routing.** Escolher o modelo por tarefa: o menor que passa no teste. Haiku busca, Sonnet implementa, Opus planeja e audita.

**Níveis de autonomia.** Quatro graus: o agente sugere; age com aprovação a cada passo; age e o humano revisa nos portões; age sozinho.

**Orquestrador.** Agente que decide na hora quais subtarefas existem e as entrega a workers. Diferente do paralelismo, em que as subtarefas são fixas antes.

**Padrões (os cinco).** Encadear, rotear, paralelizar, orquestrar, avaliar e otimizar. Dão a estrutura, e os agentes trabalham dentro dela.

**Plugin.** Pacote que reúne skills, agentes e hooks para instalar de uma vez. Aqui: `ia-na-pratica`.

**Portão.** Ponto da esteira em que o trabalho só passa se uma verificação passar: teste, revisão, aprovação humana, CI.

**Prompt caching.** Reaproveitar o início de um prompt já processado, que fica mais barato e rápido. Pede um prefixo estável.

**Prompt injection.** Instrução escondida em conteúdo que o agente lê (issue, página, documento) tentando fazer o agente obedecer a ela.

**RAG.** Buscar trechos relevantes e colocá-los no contexto antes de responder. Muda o que o modelo sabe na hora. Fine tuning muda como ele se comporta.

**Sandbox.** Isolamento do shell pelo sistema operacional. Como um container: escrita só onde é permitido e rede só para domínios liberados. No Claude Code, é o `/sandbox`.

**Skill.** Pasta com um `SKILL.md` que ensina um procedimento ao agente. A descrição é o gatilho: é por ela que o agente decide usar a skill.

**Subagente.** Agente com contexto limpo, especializado, chamado por outro. Devolve só o resumo, o que protege o contexto de quem chamou.

**Telemetria.** Registro dos eventos da sessão (ferramentas, subagentes, duração) em arquivo, para medir em vez de achar.

**Tempo de relógio.** Quanto tempo passou do início ao fim da tarefa. Inclui esperas e filas.

**Tempo humano.** Quanto tempo a pessoa gastou de fato: escrever o pedido, revisar, aprovar. É o que a esteira precisa economizar.

**Tríade letal.** Três coisas juntas num agente: dados privados, conteúdo não confiável e um canal de saída. Com as três, uma prompt injection consegue vazar dados. Corte uma perna.

**Triagem.** Primeiro passo de qualquer pedido: medir tamanho, incerteza e risco e escolher a esteira mais leve que resolve.

**Worker.** Agente que executa uma subtarefa entregue por um orquestrador.

**Workflow.** Sequência de passos escrita de antemão. Se dá para escrever os passos antes, é workflow, não agente.
