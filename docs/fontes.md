<!-- Conceito: fontes. Todo link conferido em 16/11/2026. -->

# Fontes

Cada link abaixo foi aberto e o título da página bate com o que está escrito aqui. Os textos estão em inglês.

## Fundação

* [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): Erik S. e Barry Zhang, Anthropic, 19/12/2024. Tire daqui a diferença entre workflow e agente e o princípio de começar pelo padrão mais simples.
* [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): Anthropic, 29/09/2025. Tire daqui a ideia de contexto como recurso finito e o critério de usar o menor conjunto de tokens com mais sinal.

## Conhecimento

* [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval): Anthropic, 19/09/2024. Tire daqui como acrescentar contexto a cada trecho antes de indexar para a busca errar menos.
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): documentação da Anthropic. Tire daqui como reaproveitar prefixos longos do prompt para pagar menos e responder mais rápido.
* [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills): Barry Zhang, Keith Lazuka e Mahesh Murag, Anthropic, 16/10/2025. Tire daqui a ideia de divulgação progressiva: só o nome e a descrição ficam sempre no contexto.
* [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): documentação da Anthropic. Tire daqui o formato do `SKILL.md`, os limites dos campos e os cuidados de segurança com skills de terceiros.

## Colaboração

* [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): Anthropic, 13/06/2025. Tire daqui como um agente coordenador divide o trabalho entre subagentes e o que isso custa em tokens.
* [Donating the Model Context Protocol and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation): Anthropic, 09/12/2025. Tire daqui por que o MCP passou a ter governança neutra.
* [Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation): Linux Foundation, 09/12/2025. Tire daqui quem fundou a AAIF e quais projetos ela abriga.

## Produção

* [The lethal trifecta for AI agents: private data, untrusted content, and external communication](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/): Simon Willison, 16/06/2025. Tire daqui a regra de nunca juntar dados privados, conteúdo não confiável e comunicação externa no mesmo agente.

## Documentação do Claude Code consultada

* [Extend Claude with skills](https://code.claude.com/docs/en/skills): como criar e organizar skills no Claude Code.
* [Create custom subagents](https://code.claude.com/docs/en/sub-agents): como definir subagentes, ferramentas e modelo de cada um.
* [Hooks reference](https://code.claude.com/docs/en/hooks): eventos e formato dos hooks que rodam antes e depois das ferramentas.
* [Configure permissions](https://code.claude.com/docs/en/permissions): regras de permitir, perguntar e negar.
* [Settings files and precedence](https://code.claude.com/docs/en/settings): onde ficam os arquivos de configuração e qual vence.
* [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing): como isolar os comandos do Bash.
* [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp): como ligar servidores MCP ao Claude Code.
* [How Claude remembers your project](https://code.claude.com/docs/en/memory): CLAUDE.md e memória automática.
* [Plugins overview](https://code.claude.com/docs/en/plugins): visão geral do que um plugin pode empacotar.
* [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference): campos do manifesto do plugin.
* [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference): formato do arquivo de marketplace.
* [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace): passo a passo para publicar um marketplace de plugins.

**Próximo problema:** voltar ao [mapa](00_mapa.md) e escolher o próximo conceito da aula.
