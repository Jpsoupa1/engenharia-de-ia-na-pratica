---
name: triagem
description: Classifica um pedido de código e escolhe a esteira mais leve que resolve (rápida, padrão ou completa). Use no começo de TODA tarefa que muda código, antes de planejar ou editar. Não use para perguntas ou explicações.
---

<!-- Conceito: processo proporcional à tarefa. O padrão é o mais simples; subir custa uma justificativa escrita. -->

# Triagem

Comece supondo a esteira **rápida**. Só suba se um critério abaixo obrigar, e escreva qual.

## Critérios

| Critério | Rápida | Padrão | Completa |
|---|---|---|---|
| Arquivos e camadas tocados | 1 a 3 arquivos, uma camada | vários arquivos ou duas camadas | vários módulos |
| Incerteza | passos conhecidos | precisa investigar antes | desenho em aberto |
| Risco e reversibilidade | baixo, reverte com um commit | médio | alto: dados, auth, pagamento, infra |
| Frentes independentes | nenhuma | nenhuma | duas ou mais que podem andar em paralelo |
| Tempo estimado | menos de 1 hora | 1 a 3 horas | vários dias |

Regras de desempate:
* Na dúvida entre duas, fique com a mais leve e registre o risco.
* Risco alto sobe para no mínimo padrão, mesmo que a mudança seja pequena.
* Completa só se houver frentes independentes de verdade. Tarefa grande e acoplada é padrão com mais tempo.

## Saída

Responda só com este bloco, depois siga a esteira escolhida:

```
Esteira: rápida | padrão | completa
Motivo: <uma ou duas frases citando os critérios>
Portões: <quais aprovações humanas valem: diff | plano e merge | plano, merge e segurança>
Próximo passo: <ex.: implementar e rodar os testes | usar a skill planejar>
```

As esteiras estão descritas em [esteiras/](../../../esteiras/README.md).
