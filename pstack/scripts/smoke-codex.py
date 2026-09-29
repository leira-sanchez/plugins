#!/usr/bin/env python3
"""Install and discover pstack in a temporary Codex home, without starting a model."""

import json
import os
import queue
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix="pstack-codex-") as directory:
        base = Path(directory).resolve()
        home, marketplace = base / "codex-home", base / "marketplace"
        home.mkdir()
        environment = {**os.environ, "CODEX_HOME": str(home)}
        subprocess.run([sys.executable, str(ROOT / "scripts/package-codex.py"), str(marketplace)], check=True, capture_output=True)
        for args in (
            ["plugin", "marketplace", "add", str(marketplace), "--json"],
            ["plugin", "add", "pstack@pstack-codex", "--json"],
        ):
            subprocess.run(["codex", *args], env=environment, cwd=base, check=True, capture_output=True, text=True, timeout=30)
        proc = subprocess.Popen(["codex", "app-server", "--stdio"], env=environment, cwd=base,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        messages = queue.Queue()

        def read_messages():
            for line in proc.stdout:
                messages.put(json.loads(line))
            messages.put(None)

        reader = threading.Thread(target=read_messages, daemon=True)
        reader.start()

        def send(value):
            proc.stdin.write(json.dumps(value) + "\n")
            proc.stdin.flush()

        def response(request_id):
            # Bound the whole request even if the host streams notifications.
            import time
            deadline = time.monotonic() + 30
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Codex app-server response timed out")
                message = messages.get(timeout=remaining)
                if message is None:
                    raise RuntimeError("Codex app-server exited before responding")
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(message["error"])
                    return message["result"]

        try:
            send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "pstack-smoke-test", "version": "1.0.0"}}})
            response(1)
            send({"method": "initialized"})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(base)], "forceReload": True}})
            rows = response(2)["data"]
            skills = [skill for row in rows for skill in row["skills"] if skill.get("pluginId") == "pstack@pstack-codex"]
            expected = {"pstack:" + path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
            actual = {skill["name"] for skill in skills if skill["enabled"]}
            errors = [error for row in rows for error in row.get("errors", []) if "/pstack/" in error["path"]]
            if actual != expected or errors:
                raise RuntimeError({"missing": sorted(expected - actual), "extra": sorted(actual - expected), "errors": errors})
            print(f"Codex installed pstack and discovered all {len(expected)} enabled skills without loader errors")
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            reader.join(timeout=5)
            proc.stdin.close()
            proc.stdout.close()


if __name__ == "__main__":
    main()
