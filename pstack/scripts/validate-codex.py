#!/usr/bin/env python3
"""Validate the portable resources used by pstack's Codex workflows."""

import json
import re
import sys
from pathlib import Path

import yaml


def validate(root: Path) -> list[str]:
    errors = []
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
    if manifest.get("name") != root.name or manifest.get("skills") != "./skills/":
        errors.append("manifest name or skills path does not match the plugin layout")
    for field in ("name", "version", "description", "author", "interface"):
        if not manifest.get(field):
            errors.append(f"missing manifest field: {field}")
    for field in ("logo", "composerIcon"):
        if field in manifest["interface"] and not (root / manifest["interface"][field]).is_file():
            errors.append(f"missing interface asset: {field}")
    skills = list((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    for path in skills:
        parts = path.read_text().split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"{path}: missing frontmatter")
            continue
        metadata = yaml.safe_load(parts[1])
        if not isinstance(metadata, dict):
            errors.append(f"{path}: frontmatter must be a mapping")
            continue
        if metadata.get("name") != path.parent.name or not re.fullmatch(r"[a-z0-9-]{1,64}", metadata.get("name", "")):
            errors.append(f"{path}: invalid skill name")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            errors.append(f"{path}: missing description")
        unsupported = set(metadata) - {"name", "description", "license", "allowed-tools", "metadata"}
        if unsupported:
            errors.append(f"{path}: unsupported frontmatter: {sorted(unsupported)}")
        policy = path.parent / "agents/openai.yaml"
        if policy.exists():
            invocation = yaml.safe_load(policy.read_text()).get("policy", {}).get("allow_implicit_invocation")
            if not isinstance(invocation, bool):
                errors.append(f"{policy}: invocation policy must be boolean")
    markdown = [root / "README.md"]
    for directory in ("skills", "agents", "docs"):
        markdown.extend((root / directory).rglob("*.md"))
    for path in markdown:
        if "node_modules" in path.parts:
            continue
        # Only local Markdown links; inline example paths are not file dependencies.
        for target in re.findall(r"\]\(([^)\s]+)\)", path.read_text()):
            if re.match(r"[a-z]+:", target) or target.startswith(("#", "<")):
                continue
            target = target.split("#", 1)[0]
            if not target or "*" in target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"{path}: broken local link: {target}")
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    issues = validate(root)
    if issues:
        print("\n".join(issues), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(list((root / 'skills').glob('*/SKILL.md')))} Codex skills and plugin resources")
