#!/usr/bin/env python3
"""Conceito: hook contra instrução no prompt, e verificação dentro do loop.

Hook PostToolUse (matcher "Edit|Write"). Depois de cada edição de um arquivo
TypeScript em exemplo/, roda o lint (Biome) no arquivo e só os testes afetados
(vitest related). Se algo falhar, sai com código 2 e manda o erro no stderr:
o agente recebe a mensagem e corrige no próprio loop, sem você pedir.

Edições fora de exemplo/ passam direto. Só usa a biblioteca padrão.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

LIMITE_SAIDA = 4000  # o erro volta para o contexto do agente: mande só o necessário
EXTENSOES = (".ts", ".tsx", ".js", ".mjs")


def rodar(cmd: list[str], pasta: str) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=pasta, capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return 1, f"tempo esgotado rodando: {' '.join(cmd)}"
    return r.returncode, (r.stdout + r.stderr).strip()


def main() -> int:
    try:
        dados = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    caminho = (dados.get("tool_input") or {}).get("file_path", "")
    raiz = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd())
    exemplo = os.path.join(raiz, "exemplo")
    arquivo = os.path.realpath(os.path.join(raiz, caminho)) if caminho else ""

    if not arquivo.startswith(exemplo + os.sep) or not arquivo.endswith(EXTENSOES):
        return 0
    if os.sep + "node_modules" + os.sep in arquivo:
        return 0

    binarios = os.path.join(exemplo, "node_modules", ".bin")
    biome, vitest = os.path.join(binarios, "biome"), os.path.join(binarios, "vitest")
    if not (os.path.exists(biome) and os.path.exists(vitest)):
        print("lint_e_testes.py: rode `npm install` em exemplo/ para ligar a verificação.", file=sys.stderr)
        return 1  # aviso para o humano, não bloqueia o agente

    relativo = os.path.relpath(arquivo, exemplo)
    falhas = []
    codigo, saida = rodar([biome, "check", relativo], exemplo)
    if codigo != 0:
        falhas.append(f"LINT (biome check {relativo}):\n{saida}")
    codigo, saida = rodar([vitest, "related", relativo, "--run", "--passWithNoTests", "--reporter=dot"], exemplo)
    if codigo != 0:
        falhas.append(f"TESTES (vitest related {relativo}):\n{saida}")

    if not falhas:
        return 0
    mensagem = "\n\n".join(falhas)
    if len(mensagem) > LIMITE_SAIDA:
        mensagem = mensagem[:LIMITE_SAIDA] + "\n[saída cortada]"
    print(
        f"A edição em {os.path.relpath(arquivo, raiz)} quebrou a verificação. Corrija antes de seguir.\n\n{mensagem}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
