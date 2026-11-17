#!/usr/bin/env python3
"""Conceito: observabilidade. Sem medir, "processo proporcional à tarefa" vira opinião.

Lê o JSONL gravado pelo hook .claude/hooks/telemetria.py e imprime, por sessão:

* duração de relógio (do primeiro ao último evento);
* tempo do agente trabalhando (de cada pedido até o Stop) e tempo esperando o humano;
* chamadas de ferramenta, falhas e tempo por ferramenta;
* subagentes usados e quanto tempo cada um levou;
* quantidade e tempo por tipo de evento.

Uso:
    python3 observabilidade/relatorio.py                       # lê .telemetria/
    python3 observabilidade/relatorio.py observabilidade/exemplo.jsonl
"""

from __future__ import annotations

import glob
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime


def ler(caminhos: list[str]) -> dict[str, list[dict]]:
    sessoes: dict[str, list[dict]] = defaultdict(list)
    for caminho in caminhos:
        with open(caminho, encoding="utf-8") as f:
            for numero, linha in enumerate(f, 1):
                if not linha.strip():
                    continue
                try:
                    evento = json.loads(linha)
                    evento["_t"] = datetime.fromisoformat(evento["horario"])
                except (json.JSONDecodeError, KeyError, ValueError):
                    print(f"aviso: linha {numero} de {caminho} ignorada", file=sys.stderr)
                    continue
                sessoes[evento.get("sessao", "sem_sessao")].append(evento)
    for eventos in sessoes.values():
        eventos.sort(key=lambda e: e["_t"])
    return sessoes


def fmt(segundos: float) -> str:
    if segundos < 10:
        return f"{segundos:.1f}s".replace(".", ",")
    segundos = int(round(segundos))
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    if h:
        return f"{h}h{m:02d}min"
    if m:
        return f"{m}min{s:02d}s"
    return f"{s}s"


def turnos(eventos: list[dict]) -> tuple[float, float]:
    """Soma o tempo do agente (pedido → Stop) e o tempo do humano (Stop → próximo pedido)."""
    agente = humano = 0.0
    inicio_turno = fim_turno = None
    for e in eventos:
        if e["evento"] == "UserPromptSubmit":
            if fim_turno is not None:
                humano += (e["_t"] - fim_turno).total_seconds()
                fim_turno = None
            inicio_turno = e["_t"]
        elif e["evento"] == "Stop" and inicio_turno is not None:
            agente += (e["_t"] - inicio_turno).total_seconds()
            inicio_turno, fim_turno = None, e["_t"]
    return agente, humano


def relatorio(sessao: str, eventos: list[dict]) -> str:
    inicio, fim = eventos[0]["_t"], eventos[-1]["_t"]
    agente, humano = turnos(eventos)
    chamadas = [e for e in eventos if e["evento"] in ("PostToolUse", "PostToolUseFailure")]
    falhas = sum(1 for e in chamadas if e["evento"] == "PostToolUseFailure")

    por_ferramenta: dict[str, list[float]] = defaultdict(list)
    for e in chamadas:
        por_ferramenta[e.get("ferramenta") or "?"].append((e.get("duracao_ms") or 0) / 1000)

    subagentes: dict[str, list[float]] = defaultdict(list)
    for e in eventos:
        if e["evento"] == "SubagentStop":
            subagentes[e.get("subagente") or "?"].append((e.get("duracao_ms") or 0) / 1000)

    contagem = Counter(e["evento"] for e in eventos)
    tempo_evento: dict[str, float] = defaultdict(float)
    for e in eventos:
        tempo_evento[e["evento"]] += (e.get("duracao_ms") or 0) / 1000

    linhas = [
        f"Sessão {sessao}",
        f"  Início {inicio:%d/%m %H:%M}, fim {fim:%d/%m %H:%M}",
        f"  Duração de relógio ........ {fmt((fim - inicio).total_seconds())}",
        f"  Agente trabalhando ........ {fmt(agente)}",
        f"  Esperando o humano ........ {fmt(humano)}",
        f"  Chamadas de ferramenta .... {len(chamadas)} ({falhas} com falha)",
    ]
    for nome, tempos in sorted(por_ferramenta.items(), key=lambda kv: -sum(kv[1])):
        linhas.append(f"    {nome:<22} {len(tempos):>3}x  {fmt(sum(tempos)):>9}")
    linhas.append(f"  Subagentes ................ {sum(len(t) for t in subagentes.values()) or 'nenhum'}")
    for nome, tempos in sorted(subagentes.items()):
        linhas.append(f"    {nome:<22} {len(tempos):>3}x  {fmt(sum(tempos)):>9}")
    linhas.append("  Por tipo de evento")
    for nome, qtd in contagem.most_common():
        tempo = f"{fmt(tempo_evento[nome]):>9}" if tempo_evento[nome] else ""
        linhas.append(f"    {nome:<22} {qtd:>3}x  {tempo}")
    return "\n".join(linhas)


def main(argv: list[str]) -> int:
    alvo = argv[1] if len(argv) > 1 else ".telemetria"
    caminhos = sorted(glob.glob(os.path.join(alvo, "*.jsonl"))) if os.path.isdir(alvo) else [alvo]
    caminhos = [c for c in caminhos if os.path.isfile(c)]
    if not caminhos:
        print(f"Nenhum JSONL em {alvo}. Abra uma sessão do Claude Code neste repositório e use algumas ferramentas.")
        return 1
    sessoes = ler(caminhos)
    for i, (sessao, eventos) in enumerate(sorted(sessoes.items(), key=lambda kv: kv[1][0]["_t"])):
        if i:
            print()
        print(relatorio(sessao, eventos))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
