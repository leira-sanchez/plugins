#!/usr/bin/env python3
"""Build a standalone Codex marketplace without changing the user's configuration."""

import argparse
import json
import shutil
from pathlib import Path


def package(destination: Path) -> None:
    source = Path(__file__).resolve().parents[1]
    destination = destination.expanduser().resolve()
    if destination == source or source in destination.parents:
        raise ValueError("choose an output directory outside pstack")
    destination.mkdir(parents=True, exist_ok=False)
    plugin = destination / "plugins" / "pstack"
    plugin.mkdir(parents=True)
    for name in (".codex-plugin", "skills", "agents", "assets"):
        shutil.copytree(source / name, plugin / name,
                        ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".DS_Store", "*.pyc"))
    for name in ("README.md", "LICENSE"):
        shutil.copy2(source / name, plugin / name)
    catalog = destination / ".agents" / "plugins" / "marketplace.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(json.dumps({
        "name": "pstack-codex",
        "interface": {"displayName": "pstack for Codex"},
        "plugins": [{
            "name": "pstack",
            "source": {"source": "local", "path": "./plugins/pstack"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Developer Tools",
        }],
    }, indent=2) + "\n")
    print(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new directory for the standalone marketplace")
    args = parser.parse_args()
    try:
        package(args.output)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
