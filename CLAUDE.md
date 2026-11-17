@AGENTS.md

<!-- Conceito: CLAUDE.md como mapa. Curto, carregado em toda sessão; o detalhe mora nos arquivos apontados abaixo. -->

## Claude Code

* Comece toda tarefa que muda código pela skill `triagem`. Ela escolhe a esteira; subir de esteira exige motivo escrito.
* Esteira padrão: skill `planejar`, espere a aprovação, implemente, peça ao subagente `revisor` (passe o plano e o diff), espere a aprovação do merge.
* Para achar código, use o subagente `explorador` antes de abrir arquivos no contexto principal.
* O hook `lint_e_testes.py` roda depois de cada edição em `exemplo/`. Se ele devolver erro, corrija antes de seguir.
* Antes de `/compact` ou `/clear`, use a skill `handoff`.
* Erro repetido: skill `registrar-licao`.

## Onde está cada coisa

* Conceitos da aula: `docs/` (comece por `docs/00_mapa.md`)
* Esteiras: `esteiras/`
* Skills: `.claude/skills/` · Subagentes: `.claude/agents/` · Hooks: `.claude/hooks/`
* Segurança: `seguranca/checklist.md`
