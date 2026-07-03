from __future__ import annotations

from typing import Any

CONTEXT_PROFILES: dict[str, dict[str, Any]] = {
    "micro": {
        "max_tokens": 1200,
        "purpose": "Small clarification or focused edit.",
        "agent_rule": "Do not expand files unless necessary.",
    },
    "quick": {
        "max_tokens": 3000,
        "purpose": "Default task context for common coding work.",
        "agent_rule": "Prefer canonical memory and top-ranked files.",
    },
    "debug": {
        "max_tokens": 8000,
        "purpose": "Bug investigation with tests and local failure context.",
        "agent_rule": "Include tests, likely failure files, and recent decisions.",
    },
    "architecture": {
        "max_tokens": 12000,
        "purpose": "Architecture review or cross-module planning.",
        "agent_rule": "Include decisions, graph neighborhoods, and module boundaries.",
    },
    "handoff": {
        "max_tokens": 2500,
        "purpose": "Session restart or chat compaction boundary.",
        "agent_rule": "Preserve only task state, decisions, risks, next actions, and expansion paths.",
    },
    "full": {
        "max_tokens": 20000,
        "purpose": "Large review with broad context; use sparingly.",
        "agent_rule": "Prefer summaries first and expand only when evidence is missing.",
    },
}

DEGRADATION_SIGNALS = [
    "The agent repeats previously resolved work.",
    "The agent asks for project facts already present in memory.",
    "The agent edits files outside the intended scope.",
    "The agent loses the test or validation plan.",
    "The conversation contains more process than task evidence.",
    "The prompt needs copied summaries from earlier turns.",
]

PRIORITY_ORDER = [
    "source_code",
    "git_history",
    "canonical_ai_memory",
    "machine_indexes",
    "context_packs",
    "adapter_files",
    "runtime_notes",
    "chat_history",
]


def get_context_profiles(config: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    profiles = {name: dict(profile) for name, profile in CONTEXT_PROFILES.items()}
    if config:
        configured = config.get("context", {}).get("profiles", {})
        for name, overrides in configured.items():
            if name in profiles:
                profiles[name].update(overrides)
            elif isinstance(overrides, dict) and "max_tokens" in overrides:
                profiles[name] = dict(overrides)
    return profiles


def get_profile(name: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    profiles = get_context_profiles(config)
    return profiles.get(name, profiles["quick"])


def get_budget(name: str, config: dict[str, Any] | None = None) -> int:
    return int(get_profile(name, config=config)["max_tokens"])
