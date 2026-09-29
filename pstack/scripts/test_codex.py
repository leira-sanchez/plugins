import importlib.util
import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageTests(unittest.TestCase):
    def test_catalog_resolves_complete_plugin_and_excludes_cursor_automation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "marketplace"
            load_script("package-codex").package(output)
            catalog = json.loads((output / ".agents/plugins/marketplace.json").read_text())
            plugin = output / catalog["plugins"][0]["source"]["path"]
            self.assertEqual(load_script("validate-codex").validate(plugin), [])
            self.assertEqual(
                {p.parent.name for p in (plugin / "skills").glob("*/SKILL.md")},
                {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")},
            )
            self.assertTrue((plugin / "skills/poteto-mode/scripts/watch-pr/watch-pr").is_file())
            self.assertTrue((plugin / "agents/comment-sicko.md").is_file())
            self.assertFalse((plugin / "automations").exists())
            self.assertFalse((plugin / ".cursor-plugin").exists())
            self.assertEqual(list(plugin.rglob("node_modules")), [])

    def test_packaging_refuses_existing_output_without_modifying_it(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            sentinel = output / "keep.txt"
            sentinel.write_text("user data")
            with self.assertRaises(FileExistsError):
                load_script("package-codex").package(output)
            self.assertEqual(sentinel.read_text(), "user data")
            self.assertEqual(list(output.iterdir()), [sentinel])


class WorktreeAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "main repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "--allow-empty", "-m", "base")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.worktree = self.base / "worker [one]"
        self.git("worktree", "add", "-b", "worker", str(self.worktree))
        self.bin = self.base / "bin"
        self.bin.mkdir()
        # The audit must not reach a real GitHub repository in this fixture.
        gh = self.bin / "gh"
        gh.write_text('#!/bin/sh\nprintf "[]\\n"\n')
        gh.chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"]}
        self.script = ROOT / "skills/poteto-mode/scripts/worktree-audit.sh"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True, text=True)

    def audit(self, history=None):
        args = ["bash", str(self.script), str(self.repo)]
        if history:
            args.append(str(history))
        result = subprocess.run(args, env=self.env, check=True, capture_output=True, text=True)
        rows = result.stdout.strip().splitlines()
        self.assertEqual(len(rows), 2, result.stdout)
        return dict(zip(rows[0].split("\t"), rows[1].split("\t")))

    def test_missing_history_is_unknown_even_for_merged_worktree_with_spaces(self):
        row = self.audit()
        self.assertEqual(row["WORKTREE"], str(self.worktree))
        self.assertEqual(row["MERGED"], "YES")
        self.assertEqual(row["LAST_CHAT"], "unknown")
        self.assertEqual(row["BUCKET"], "review-history")

    def test_recent_workspace_history_holds_candidate_and_ignores_prefix_collision(self):
        history = self.base / "scoped history"
        history.mkdir()
        exact = history / "old.jsonl"
        exact.write_text(json.dumps({"cwd": str(self.worktree)}))
        old = time.time() - 10 * 86400
        os.utime(exact, (old, old))
        (history / "unrelated.jsonl").write_text(json.dumps({"cwd": str(self.worktree) + "-other"}))
        self.assertEqual(self.audit(history)["BUCKET"], "safe")
        os.utime(exact, None)
        self.assertEqual(self.audit(history)["BUCKET"], "verify-recent-chat")

    def test_symlinked_history_outside_scope_is_not_read(self):
        history = self.base / "scoped"
        history.mkdir()
        private = self.base / "other-project.jsonl"
        private.write_text(json.dumps({"cwd": str(self.worktree)}))
        (history / "linked.jsonl").symlink_to(private)
        self.assertEqual(self.audit(history)["LAST_CHAT"], "unknown")


if __name__ == "__main__":
    unittest.main()
