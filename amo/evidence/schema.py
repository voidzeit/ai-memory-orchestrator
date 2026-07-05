from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


EVIDENCE_KINDS = {
    "scan",
    "graph_build",
    "validation",
    "benchmark",
    "context_pack",
    "handoff",
    "postflight",
    "optimizer_trial",
    "adapter_export",
    "mcp_tool_invocation",
}


@dataclass(frozen=True)
class EvidenceEntry:
    kind: str
    source: str
    result: str
    authority: float
    timestamp: str = ""
    commit: str | None = None
    artifacts: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in EVIDENCE_KINDS:
            raise ValueError(f"Unknown evidence kind '{self.kind}'")
        if not 0.0 <= self.authority <= 1.0:
            raise ValueError("authority must be between 0.0 and 1.0")
        if not self.source:
            raise ValueError("source is required")
        if not self.timestamp:
            object.__setattr__(self, "timestamp", datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, object]:
        return {
            "timestamp": self.timestamp,
            "kind": self.kind,
            "source": self.source,
            "result": self.result,
            "commit": self.commit,
            "authority": self.authority,
            "artifacts": list(self.artifacts),
            "limitations": list(self.limitations),
        }
