from __future__ import annotations

from pathlib import Path

RESOURCES: dict[str, dict[str, str]] = {
    "amo://memory/state": {
        "path": ".ai/state.md",
        "name": "Project state",
        "description": "Canonical current-truth memory.",
        "mimeType": "text/markdown",
    },
    "amo://memory/tasks": {
        "path": ".ai/tasks.md",
        "name": "Open tasks",
        "description": "Canonical task memory.",
        "mimeType": "text/markdown",
    },
    "amo://memory/decisions": {
        "path": ".ai/decisions.md",
        "name": "Decisions",
        "description": "Canonical decision log.",
        "mimeType": "text/markdown",
    },
    "amo://memory/tests": {
        "path": ".ai/tests.md",
        "name": "Validation commands",
        "description": "Canonical test and validation memory.",
        "mimeType": "text/markdown",
    },
    "amo://graph": {
        "path": ".ai/machine/graph.json",
        "name": "Project graph",
        "description": "Derived knowledge graph (nodes and edges).",
        "mimeType": "application/json",
    },
    "amo://validation": {
        "path": ".ai/machine/validation.json",
        "name": "Validation result",
        "description": "Latest validation status and warnings.",
        "mimeType": "application/json",
    },
    "amo://context/quick": {
        "path": ".ai/packs/quick.md",
        "name": "Quick context pack",
        "description": "Latest compiled quick-profile context pack.",
        "mimeType": "text/markdown",
    },
    "amo://handoff/latest": {
        "path": ".ai/packs/handoff.md",
        "name": "Latest handoff",
        "description": "Latest compiled session handoff pack.",
        "mimeType": "text/markdown",
    },
    "amo://benchmark/latest": {
        "path": ".ai/machine/benchmark.json",
        "name": "Latest benchmark",
        "description": "Latest benchmark metrics.",
        "mimeType": "application/json",
    },
    "amo://evolution/findings": {
        "path": ".ai/evolution/findings.md",
        "name": "Optimizer findings",
        "description": "Latest deterministic optimizer findings.",
        "mimeType": "text/markdown",
    },
}


def list_resources() -> list[dict[str, str]]:
    return [
        {
            "uri": uri,
            "name": meta["name"],
            "description": meta["description"],
            "mimeType": meta["mimeType"],
        }
        for uri, meta in RESOURCES.items()
    ]


def read_resource(repo: Path, uri: str) -> dict[str, str]:
    meta = RESOURCES.get(uri)
    if meta is None:
        raise KeyError(f"Unknown resource: {uri}")
    path = repo.resolve() / meta["path"]
    if not path.exists():
        raise FileNotFoundError(f"Resource not generated yet: {meta['path']}")
    return {"uri": uri, "mimeType": meta["mimeType"], "text": path.read_text(encoding="utf-8")}
