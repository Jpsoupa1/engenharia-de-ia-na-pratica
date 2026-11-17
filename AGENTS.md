<!-- Conceito: memória semântica portável. Vale para qualquer agente que leia AGENTS.md; o CLAUDE.md importa este arquivo. -->

# AGENTS.md

## O projeto
Material de apoio da aula "Engenharia de IA na prática". O código executável é pequeno:
* `exemplo/`: lista de tarefas em TypeScript para praticar a esteira.
* `.claude/hooks/`: hooks em Python 3, só biblioteca padrão.
* `observabilidade/relatorio.py`: lê a telemetria.

O resto é documentação em português.

## Comandos
* Testar o exemplo: `cd exemplo && npm test`
* Lint, tipos e testes juntos: `cd exemplo && npm run verificar`
* Testar os hooks: `python3 .claude/hooks/test_hooks.py -v`
* Relatório de telemetria: `python3 observabilidade/relatorio.py`

## Regras que valem sempre
* Critérios de aceite antes do código. Cada critério vira teste, inclusive o caso negado.
* Pronto = `npm run verificar` passando e o diff revisado.
* Uma mudança por vez: uma hipótese, uma mudança, um teste.
* Nunca leia nem grave `.env`, chaves ou tokens. Credencial só por variável de ambiente.
* Nada de deploy, push forçado ou push na `main` pelo agente.
* Escrita em português do Brasil, frases curtas, sem travessão.
* Não implemente o filtro por data em `exemplo/`: ele é o exercício.
