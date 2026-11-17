#!/usr/bin/env python3
"""Conceito: guardrail determinístico e menor privilégio.

Hook PreToolUse (matcher "Bash"). Lê o comando que o agente quer rodar e
nega, com o motivo, os padrões perigosos:

* apagar recursivamente fora do projeto;
* push forçado;
* ler .env, chaves e credenciais;
* comandos de deploy (deploy sai pelo CI, nunca da máquina do agente).

Uma regra no prompt o modelo pode esquecer. Este código roda sempre.
Só usa a biblioteca padrão do Python 3, funciona em macOS e Linux.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

SEPARADORES = re.compile(r"&&|\|\||[;|\n]")

ENV_PERMITIDOS = re.compile(r"\.env\.(exemplo|example|sample|modelo)$")
ARQUIVO_SENSIVEL = re.compile(
    r"(^|/)\.env(\.[\w.-]+)?$"  # .env, .env.local, .env.production
    r"|(^|/)id_(rsa|ed25519|ecdsa|dsa)$"  # chaves SSH privadas
    r"|\.(pem|key|p12|pfx)$"  # certificados e chaves
    r"|(^|/)\.ssh/"
    r"|(^|/)\.aws/credentials$"
    r"|(^|/)\.netrc$"
)

DEPLOY = [
    (re.compile(r"\bvercel\b.*(--prod\b|\bdeploy\b)"), "vercel"),
    (re.compile(r"\bnetlify\s+deploy\b"), "netlify deploy"),
    (re.compile(r"\b(fly|flyctl)\s+deploy\b"), "fly deploy"),
    (re.compile(r"\bfirebase\s+deploy\b"), "firebase deploy"),
    (re.compile(r"\bkubectl\s+(apply|delete|rollout)\b"), "kubectl"),
    (re.compile(r"\bterraform\s+(apply|destroy)\b"), "terraform"),
    (re.compile(r"\bhelm\s+(install|upgrade|uninstall)\b"), "helm"),
    (re.compile(r"\b(npm|pnpm|yarn)\s+publish\b"), "publicar pacote"),
    (re.compile(r"\bsupabase\s+db\s+push\b"), "supabase db push"),
    (re.compile(r"\bgit\s+push\b.*\b(production|producao|prod)\b"), "push para produção"),
]


def raiz_do_projeto(dados: dict) -> str:
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or dados.get("cwd") or os.getcwd())


def tokens(trecho: str) -> list[str]:
    try:
        return shlex.split(trecho)
    except ValueError:  # aspas desbalanceadas: cai para uma divisão simples
        return trecho.split()


def dentro(caminho: str, raiz: str) -> bool:
    return caminho == raiz or caminho.startswith(raiz + os.sep)


def checar_rm(partes: list[str], cwd: str, raiz: str) -> str | None:
    if not partes or os.path.basename(partes[0]) != "rm":
        return None
    flags = [p for p in partes[1:] if p.startswith("-")]
    recursivo = any(f in ("-r", "-R", "--recursive") or (not f.startswith("--") and ("r" in f or "R" in f)) for f in flags)
    if not recursivo:
        return None
    alvos = [p for p in partes[1:] if not p.startswith("-")]
    for alvo in alvos:
        if "$" in alvo or "`" in alvo:
            return f"rm recursivo com variável ({alvo}): não dá para saber o alvo antes de rodar."
        absoluto = os.path.realpath(os.path.join(cwd, os.path.expanduser(alvo)))
        if not dentro(absoluto, raiz) or absoluto == raiz:
            return f"rm recursivo fora do projeto (ou na raiz dele): {alvo}."
    return None


def checar_push(partes: list[str]) -> str | None:
    if len(partes) < 2 or partes[0] != "git" or "push" not in partes[1:3]:
        return None
    for p in partes:
        if p in ("-f", "--force", "--force-with-lease", "--force-if-includes") or p.startswith("--force"):
            return "push forçado reescreve o histórico remoto e pode apagar trabalho de outras pessoas."
        if p.startswith("+") and len(p) > 1:
            return f"refspec com + ({p}) é um push forçado."
        if p.startswith("-") and not p.startswith("--") and "f" in p:
            return "push forçado reescreve o histórico remoto e pode apagar trabalho de outras pessoas."
    return None


def checar_segredo(partes: list[str]) -> str | None:
    for p in partes:
        alvo = p.split("=", 1)[-1] if p.startswith("-") and "=" in p else p
        if ENV_PERMITIDOS.search(alvo):
            continue
        if ARQUIVO_SENSIVEL.search(alvo):
            return f"o comando toca um arquivo de segredo ({alvo}). Segredo fica fora do contexto do agente."
    return None


def checar_deploy(trecho: str) -> str | None:
    for padrao, nome in DEPLOY:
        if padrao.search(trecho):
            return f"comando de deploy ({nome}). Deploy sai pelo CI, com aprovação humana, nunca do agente."
    return None


def avaliar(comando: str, cwd: str, raiz: str) -> str | None:
    for trecho in SEPARADORES.split(comando):
        trecho = trecho.strip()
        if not trecho:
            continue
        partes = tokens(trecho)
        while partes and (partes[0] in ("sudo", "env", "command", "exec") or "=" in partes[0]):
            partes = partes[1:]  # "sudo rm", "FOO=1 rm": olha o comando de verdade
        for checagem in (
            lambda: checar_rm(partes, cwd, raiz),
            lambda: checar_push(partes),
            lambda: checar_segredo(partes),
            lambda: checar_deploy(trecho),
        ):
            motivo = checagem()
            if motivo:
                return motivo
    return None


def main() -> int:
    try:
        dados = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # entrada estranha: não bloqueia, mas também não decide nada
    if dados.get("tool_name") != "Bash":
        return 0
    comando = (dados.get("tool_input") or {}).get("command", "")
    raiz = raiz_do_projeto(dados)
    cwd = os.path.realpath(dados.get("cwd") or raiz)
    motivo = avaliar(comando, cwd, raiz)
    if motivo is None:
        return 0
    resposta = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Bloqueado pelo hook bloquear_perigosos.py: {motivo} "
                "Se for mesmo necessário, explique ao humano e peça para ele rodar."
            ),
        }
    }
    print(json.dumps(resposta, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
