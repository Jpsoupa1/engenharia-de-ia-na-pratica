---
name: planejar
description: Gera o plano de uma tarefa padrão ou completa no formato do template (objetivo, arquivos, passos, critérios de aceite, testes, riscos, fora do escopo) e pede aprovação humana antes de qualquer código. Use depois que a triagem escolher padrão ou completa, ou quando pedirem um plano.
---

<!-- Conceito: plano antes do código e portão humano. Errar no plano custa minutos; errar no código custa horas. -->

# Planejar

1. Leia o mínimo para planejar: use o subagente `explorador` para mapear os arquivos relevantes. Não leia o repositório inteiro.
2. Preencha [template_plano.md](template_plano.md). Cada seção é obrigatória; se não houver risco, escreva "nenhum identificado".
3. Critérios de aceite são verificáveis: cada um vira pelo menos um teste. Inclua o caso negado (entrada inválida, permissão recusada), não só o caminho feliz.
4. "Fora do escopo" protege contra crescimento silencioso. Liste o que é tentador e não entra.
5. Quer ver um plano pronto? Abra [exemplos/feature_filtro_data.md](exemplos/feature_filtro_data.md) só se precisar de referência.

Termine sempre com:

> **Aprovação necessária.** Responda "aprovado" para eu implementar, ou diga o que mudar no plano.

Não escreva código até receber a aprovação.
