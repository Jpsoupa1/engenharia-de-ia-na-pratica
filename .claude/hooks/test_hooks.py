#!/usr/bin/env python3
"""Conceito: o teste cobre o caso negado, não só o permitido.

Roda cada hook com uma entrada JSON simulada, do mesmo jeito que o Claude Code
chama: JSON no stdin, resposta no stdout, stderr e código de saída.

Uso: python3 .claude/hooks/test_hooks.py -v   (na raiz do repositório)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(PASTA))


def chamar(hook: str, entrada: dict, projeto: str = RAIZ) -> subprocess.CompletedProcess:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": projeto}
    return subprocess.run(
        [sys.executable, os.path.join(PASTA, hook)],
        input=json.dumps(entrada),
        capture_output=True,
        text=True,
        env=env,
        timeout=180,
    )


def bash(comando: str, cwd: str = RAIZ) -> dict:
    return {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": comando}, "cwd": cwd}


class BloquearPerigosos(unittest.TestCase):
    def decisao(self, comando: str) -> str:
        r = chamar("bloquear_perigosos.py", bash(comando))
        self.assertEqual(r.returncode, 0, r.stderr)
        if not r.stdout.strip():
            return "segue"
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]

    def test_nega_comandos_perigosos(self):
        perigosos = [
            "rm -rf /",
            "rm -rf ~/projetos",
            "rm -rf ../outro_repo",
            "rm -fr .",
            "sudo rm -r /var/log",
            "cd exemplo && rm -rf $ALVO",
            "git push --force origin main",
            "git push -f",
            "git push origin +main",
            "cat .env",
            "grep TOKEN exemplo/.env.local",
            "source .env && npm start",
            "cat ~/.ssh/id_ed25519",
            "vercel --prod",
            "npm publish",
            "terraform apply -auto-approve",
            "kubectl apply -f k8s/",
        ]
        for comando in perigosos:
            with self.subTest(comando=comando):
                self.assertEqual(self.decisao(comando), "deny")

    def test_deixa_passar_comandos_normais(self):
        normais = [
            "npm test",
            "cd exemplo && npm run lint",
            "rm -rf exemplo/node_modules",
            "rm arquivo_solto.txt",
            "git push origin minha-branch",
            "git commit -m 'corrige o loader do .env'",
            "cat .env.exemplo",
            "ls -la",
            "python3 observabilidade/relatorio.py",
        ]
        for comando in normais:
            with self.subTest(comando=comando):
                self.assertEqual(self.decisao(comando), "segue")

    def test_motivo_chega_ao_agente(self):
        r = chamar("bloquear_perigosos.py", bash("git push --force"))
        motivo = json.loads(r.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("push forçado", motivo)

    def test_ignora_outras_ferramentas(self):
        r = chamar("bloquear_perigosos.py", {"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {}})
        self.assertEqual((r.returncode, r.stdout), (0, ""))


@unittest.skipUnless(os.path.exists(os.path.join(RAIZ, "exemplo", "node_modules", ".bin", "vitest")), "rode npm install em exemplo/")
class LintETestes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        destino = os.path.join(self.tmp, "exemplo")
        shutil.copytree(os.path.join(RAIZ, "exemplo"), destino, ignore=shutil.ignore_patterns("node_modules"))
        os.symlink(os.path.join(RAIZ, "exemplo", "node_modules"), os.path.join(destino, "node_modules"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def editar(self, caminho: str) -> subprocess.CompletedProcess:
        entrada = {"hook_event_name": "PostToolUse", "tool_name": "Edit", "tool_input": {"file_path": caminho}}
        return chamar("lint_e_testes.py", entrada, projeto=self.tmp)

    def test_passa_quando_esta_tudo_certo(self):
        r = self.editar(os.path.join(self.tmp, "exemplo", "src", "listar.ts"))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_devolve_o_erro_quando_quebra_um_teste(self):
        arquivo = os.path.join(self.tmp, "exemplo", "src", "listar.ts")
        with open(arquivo) as f:
            codigo = f.read()
        with open(arquivo, "w") as f:  # bug de propósito: inverte o filtro
            f.write(codigo.replace("tarefa.status === status", "tarefa.status !== status"))
        r = self.editar(arquivo)
        self.assertEqual(r.returncode, 2)
        self.assertIn("TESTES", r.stderr)
        self.assertIn("filtrarPorStatus", r.stderr)

    def test_ignora_arquivo_fora_do_exemplo(self):
        r = self.editar(os.path.join(self.tmp, "docs", "01_fundacao.md"))
        self.assertEqual((r.returncode, r.stderr), (0, ""))


class Telemetria(unittest.TestCase):
    def test_grava_jsonl_com_duracao_e_sem_conteudo(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = {"session_id": "s1", "tool_name": "Bash", "tool_use_id": "t1", "tool_input": {"command": "cat segredo"}}
            for evento in ("PreToolUse", "PostToolUse"):
                self.assertEqual(chamar("telemetria.py", {**base, "hook_event_name": evento}, projeto=tmp).returncode, 0)
            sub = {"session_id": "s1", "agent_id": "a1", "agent_type": "explorador"}
            for evento in ("SubagentStart", "SubagentStop"):
                chamar("telemetria.py", {**sub, "hook_event_name": evento}, projeto=tmp)
            with open(os.path.join(tmp, ".telemetria", "s1.jsonl")) as f:
                linhas = [json.loads(linha) for linha in f]
            self.assertEqual([l["evento"] for l in linhas], ["PreToolUse", "PostToolUse", "SubagentStart", "SubagentStop"])
            self.assertIsInstance(linhas[1]["duracao_ms"], int)
            self.assertEqual(linhas[3]["subagente"], "explorador")
            self.assertIsInstance(linhas[3]["duracao_ms"], int)
            self.assertNotIn("segredo", json.dumps(linhas))

    def test_entrada_invalida_nao_quebra(self):
        r = subprocess.run([sys.executable, os.path.join(PASTA, "telemetria.py")], input="não é json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


class Relatorio(unittest.TestCase):
    def test_le_o_jsonl_de_exemplo(self):
        script = os.path.join(RAIZ, "observabilidade", "relatorio.py")
        r = subprocess.run([sys.executable, script, os.path.join(RAIZ, "observabilidade", "exemplo.jsonl")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Sessão", r.stdout)
        self.assertIn("explorador", r.stdout)


if __name__ == "__main__":
    unittest.main()
