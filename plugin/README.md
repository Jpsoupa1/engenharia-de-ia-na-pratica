<!-- Conceito: escala no nível do time. O que funciona no seu projeto vira um pacote que o time instala com um comando. -->

# Plugin `ia-na-pratica`

Este repositório também é um **marketplace** com um **plugin**. O plugin empacota:

| Componente | De onde vem |
|---|---|
| Skills `triagem`, `planejar`, `revisar`, `registrar-licao`, `handoff` | `.claude/skills/` |
| Subagentes `explorador`, `revisor`, `seguranca` | `.claude/agents/` |
| Hooks `bloquear_perigosos.py` e `telemetria.py` | `plugin/hooks.json` aponta para `.claude/hooks/` |

## Por que os manifestos ficam na raiz

Um plugin não pode apontar para arquivos fora da própria pasta: na instalação ele é copiado para um cache, e o que está fora não vai junto. Por isso a raiz do plugin é a raiz do repositório:

* `.claude-plugin/plugin.json`: o manifesto, com `skills`, `agents` e `hooks` apontando para `./.claude/...` e `./plugin/hooks.json`;
* `.claude-plugin/marketplace.json`: o catálogo, com uma entrada `"source": "./"`.

Assim existe uma cópia só de cada skill. O que você testa no repositório é o que o time instala.

## Por que `lint_e_testes.py` fica de fora

Ele roda os comandos de **este** projeto de exemplo. No projeto de outra pessoa os comandos são outros. Hook que depende do projeto mora no `.claude/settings.json` do projeto. Hook que vale em qualquer lugar (bloquear comando perigoso, medir) vai no plugin.

## Como o time instala

Dentro do Claude Code, em um passo:

```
/plugin install ia-na-pratica --marketplace <dono>/engenharia-de-ia-na-pratica
```

Ou em dois passos (adiciona o marketplace e depois instala):

```
/plugin marketplace add <dono>/engenharia-de-ia-na-pratica
/plugin install ia-na-pratica@engenharia-de-ia-na-pratica
```

Ou pelo terminal:

```bash
claude plugin marketplace add <dono>/engenharia-de-ia-na-pratica
claude plugin install ia-na-pratica@engenharia-de-ia-na-pratica
```

Troque `<dono>` pelo usuário ou organização do GitHub onde o repositório está.

As skills do plugin ganham o prefixo do plugin: `/ia-na-pratica:triagem`. Isso evita colisão com uma skill pessoal de mesmo nome.

Para o time inteiro receber a sugestão de instalar ao abrir um repositório, declare no `.claude/settings.json` desse repositório:

```json
{
  "extraKnownMarketplaces": {
    "engenharia-de-ia-na-pratica": {
      "source": { "source": "github", "repo": "<dono>/engenharia-de-ia-na-pratica" }
    }
  },
  "enabledPlugins": { "ia-na-pratica@engenharia-de-ia-na-pratica": true }
}
```

A telemetria do plugin grava em `.telemetria/` na raiz do seu projeto: acrescente essa pasta ao `.gitignore`.

## Testar antes de publicar

```bash
claude plugin validate .        # confere os manifestos
claude --plugin-dir .           # abre uma sessão com o plugin carregado do disco
```

Ao mudar o plugin, suba o campo `version` do `plugin.json`. Sem isso, quem já instalou não recebe a mudança.

**Próximo problema:** um pacote instalado por várias pessoas precisa de prova de que funciona. Veja [evals/](../evals/README.md).
