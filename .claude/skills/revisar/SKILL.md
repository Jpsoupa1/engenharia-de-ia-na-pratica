---
name: revisar
description: Revisa um diff contra o plano aprovado com um checklist de escopo, testes, legibilidade e segurança básica, em no máximo duas rodadas. Use depois da implementação e antes do portão de merge, de preferência dentro do subagente revisor.
---

<!-- Conceito: avaliar e otimizar, com critério de parada. Quem gera não avalia. -->

# Revisar

Entrada: o plano aprovado e o diff (`git diff` contra a branch base).

## Checklist

**Escopo**
* [ ] Toda mudança do diff está prevista no plano.
* [ ] Nada do "fora do escopo" entrou.

**Testes**
* [ ] Cada critério de aceite tem teste.
* [ ] Existe teste para o caso negado.
* [ ] `npm run verificar` passa em `exemplo/` (lint, tipos e testes).

**Legibilidade**
* [ ] Nomes dizem o que a coisa faz.
* [ ] Sem código morto, sem comentário que repete o código.

**Segurança básica**
* [ ] Nenhum segredo, token ou dado pessoal no diff.
* [ ] Entrada externa validada antes do uso.
* [ ] Nenhuma permissão ou dependência nova sem justificativa.

## Saída

```
Rodada: 1 | 2
Veredito: aprovado | reprovado
Problemas: <lista curta: arquivo:linha, o que está errado, o que fazer>
```

## Critério de parada

No máximo **duas rodadas**. Se a segunda rodada reprovar, pare e chame o humano com os problemas que sobraram. Uma terceira rodada costuma girar em círculo e gastar tokens sem convergir.
