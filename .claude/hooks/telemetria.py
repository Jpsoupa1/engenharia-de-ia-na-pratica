#!/usr/bin/env python3
"""Conceito: observabilidade.

Hook ligado em vários eventos (veja .claude/settings.json). Grava uma linha
JSONL por evento em .telemetria/<sessao>.jsonl, pasta ignorada pelo git.

Campos: horario, sessao, evento, ferramenta, subagente, duracao_ms.
A duração sai do par PreToolUse e PostToolUse com o mesmo tool_use_id
(e do par SubagentStart e SubagentStop com o mesmo agent_id).

De propósito NÃO grava o conteúdo: nem prompt, nem comando, nem saída.
Telemetria que copia o contexto vira um novo lugar para vazar segredo.

Nunca bloqueia nada: qualquer erro aqui é engolido e o hook sai com 0.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone

INICIO = {"PreToolUse": "ferramenta", "SubagentStart": "subagente"}
FIM = {"PostToolUse": "ferramenta", "PostToolUseFailure": "ferramenta", "SubagentStop": "subagente"}


def seguro(texto: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", texto)[:120] or "sem_id"


def chave(dados: dict, tipo: str) -> str | None:
    valor = dados.get("tool_use_id") if tipo == "ferramenta" else dados.get("agent_id")
    return f"{tipo}_{seguro(valor)}" if valor else None


def registrar(dados: dict) -> None:
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd()
    pasta = os.path.join(raiz, ".telemetria")
    pendentes = os.path.join(pasta, ".pendentes")
    os.makedirs(pendentes, exist_ok=True)

    evento = dados.get("hook_event_name", "desconhecido")
    sessao = seguro(dados.get("session_id", "sem_sessao"))
    agora = time.time()
    duracao_ms = None

    if evento in INICIO and (k := chave(dados, INICIO[evento])):
        with open(os.path.join(pendentes, k), "w") as f:
            f.write(str(agora))
    elif evento in FIM and (k := chave(dados, FIM[evento])):
        marca = os.path.join(pendentes, k)
        try:
            with open(marca) as f:
                duracao_ms = round((agora - float(f.read())) * 1000)
            os.remove(marca)
        except (OSError, ValueError):
            pass

    linha = {
        "horario": datetime.fromtimestamp(agora, timezone.utc).isoformat(timespec="milliseconds"),
        "sessao": sessao,
        "evento": evento,
        "ferramenta": dados.get("tool_name"),
        "subagente": dados.get("agent_type") or dados.get("agent_id"),
        "duracao_ms": duracao_ms,
    }
    with open(os.path.join(pasta, f"{sessao}.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def main() -> int:
    try:
        registrar(json.load(sys.stdin))
    except Exception:  # observabilidade nunca derruba o trabalho
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
