<!-- Conceito: observabilidade e telemetria, medir tempo de relógio e tempo humano para provar a esteira certa. -->
# Observabilidade

Para saber, meça. Sem medida, "essa esteira parece lenta" é só impressão.

## A história do 3h para 15h

Uma tarefa de cerca de 3 horas passou a levar cerca de 15 quando o processo completo (plano, subagentes, revisão, auditoria) era usado em tudo, até em mudanças pequenas. Ninguém decidiu isso. Foi acumulando, etapa por etapa. A correção veio de medir: onde o tempo ia, e qual etapa não se pagava. Daí nasceu a regra de [esteiras](../esteiras/README.md) proporcionais à tarefa.

## Dois tempos

* **Tempo de relógio:** do início ao fim da tarefa. Inclui espera, fila e o agente trabalhando.
* **Tempo humano:** o tempo que você realmente gastou: pedir, ler o plano, revisar, aprovar.

Um agente pode levar 40 minutos de relógio e só 5 de tempo humano. É um bom resultado. Se o relógio é curto mas o tempo humano é alto, o agente deu trabalho de revisão demais. Meça os dois.

## O que é gravado

O hook [telemetria.py](../.claude/hooks/telemetria.py) grava um JSONL em `.telemetria/` (ignorada pelo git). Cada linha tem:

* `horario`
* `sessao`
* `evento`
* `ferramenta`
* `subagente`
* `duracao_ms`

Eventos: início e fim de sessão, cada pedido seu, antes e depois de cada ferramenta, falha de ferramenta, início e fim de subagente e cada vez que o agente para e devolve a vez. O conteúdo (prompt, comando, saída) nunca é gravado.

## Rodar o relatório

Primeiro com o arquivo de exemplo, que já vem no repositório:

```bash
python3 observabilidade/relatorio.py observabilidade/exemplo.jsonl
```

Depois com os seus dados, depois de algumas sessões com o plugin ou os hooks ativos:

```bash
python3 observabilidade/relatorio.py .telemetria/
```

## Como ler

A sessão `exemplo_padrao` do arquivo de exemplo é uma esteira padrão: plano, aprovação, implementação, revisão e merge.

```
Sessão exemplo_padrao
  Duração de relógio ........ 46min37s
  Agente trabalhando ........ 5min27s
  Esperando o humano ........ 40min00s
  Chamadas de ferramenta .... 15 (1 com falha)
  Subagentes ................ 2
    explorador               1x        38s
    revisor                  1x        56s
```

* **Duração de relógio:** do primeiro ao último evento.
* **Agente trabalhando:** soma dos trechos entre cada pedido seu e o momento em que o agente para.
* **Esperando o humano:** soma dos trechos entre o agente parar e o seu próximo pedido. É onde mora o tempo humano: ler o plano, revisar, aprovar. No exemplo, 40 dos 46 minutos foram de espera nos dois portões. Se o portão é o gargalo, o plano ou o diff está grande demais para revisar rápido.
* **Chamadas de ferramenta:** por ferramenta, com o tempo. Muitas chamadas com pouca mudança sugere o agente rodando em círculos.
* **Subagentes:** quantos e quanto tempo. Cada um custa contexto e tokens.
* **Por tipo de evento:** contagem de cada evento e o tempo somado onde há duração.

Perguntas para fazer ao ler:

* A esteira escolhida foi proporcional? Uma rápida com cinco subagentes não foi.
* Um hook de teste lento está pesando no loop?
* O mesmo erro apareceu duas vezes? Vira regra, teste ou hook.

## Ligando com os evals

Cada execução de um [caso](../evals/casos.md) usa o tempo de relógio do relatório. Compare antes e depois de mudar modelo, skill ou CLAUDE.md.

## Privacidade

A telemetria guarda nomes de ferramentas e tempos, não o conteúdo dos arquivos. Mesmo assim, não suba `.telemetria/` para o repositório.

**Próximo problema:** o agente lê conteúdo de terceiros e pode ser enganado. Veja o [checklist de segurança](../seguranca/checklist.md).
