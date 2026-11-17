<!-- Conceito: vault de notas como memória do agente. O modelo não tem estado, mas o vault tem. -->
# Vault de exemplo

Este vault guarda o conhecimento do projeto entre sessões. O modelo não tem estado, o vault tem.

## Mapa

* `projetos/<nome>/indice.md`: ponto de entrada de cada projeto. Resumo no topo e links para o resto.
* `decisoes/`: ADRs numerados, uma decisão por arquivo.
* `sessoes/`: uma nota por sessão de trabalho, criada pelo handoff.
* `templates/`: modelos de plano, ADR e sessão.

## Regras de leitura (com orçamento)

1. Comece pelo índice do projeto. O resumo no topo costuma bastar.
2. Leia só as notas ligadas à tarefa. Siga os links do índice, não varra a pasta.
3. Orçamento: no máximo 3 notas numa tarefa padrão. Na rápida, nenhuma além do resumo. Na completa, até 8.
4. Se a nota parecer velha, confira contra o código antes de confiar. Memória velha é pior que nenhuma.

## Regras de escrita

* Uma decisão difícil de reverter vira ADR, a partir do template.
* Ao fim da sessão, o handoff grava a nota de sessão: objetivo, decisões, estado, próximos passos e lições.
* Uma lição durável vira regra, teste ou hook, e a nota aponta para onde.
* Atualize o resumo do índice quando o estado do projeto mudar.
* **Nunca grave segredo no vault.** Nem token, senha, chave ou conteúdo de `.env`.

**Próximo problema:** ver o vault em uso, pelo [índice do projeto de exemplo](projetos/exemplo/indice.md).
