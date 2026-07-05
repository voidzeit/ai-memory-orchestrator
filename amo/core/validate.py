from pathlib import Path

from amo.evidence.ledger import record_evidence
from amo.io import write_json
from amo.paths import CANONICAL_FILES, ai_path
from amo.validators.artifacts import check_runtime_pollution
from amo.validators.graph import check_graph_contract
from amo.validators.instructions import check_unsafe_instructions
from amo.validators.references import check_missing_canonical_files


def validate_repo(repo: Path, strict: bool = False) -> dict[str, object]:
    repo = repo.resolve()
    warnings: list[str] = []
    warnings.extend(check_missing_canonical_files(repo, CANONICAL_FILES))
    warnings.extend(check_runtime_pollution(repo))
    warnings.extend(check_graph_contract(repo))
    warnings.extend(check_unsafe_instructions(repo))
    status = "green" if not warnings else "yellow"
    if strict and warnings:
        status = "red"
    result = {"status": status, "warnings": warnings}
    write_json(ai_path(repo, "machine", "validation.json"), result)
    record_evidence(
        repo,
        kind="validation",
        source="amo validate --strict" if strict else "amo validate",
        result=status,
        authority=0.9,
        artifacts=(".ai/machine/validation.json",),
        limitations=("does not prove production readiness",),
    )
    return result
