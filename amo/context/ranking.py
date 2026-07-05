from typing import Any


DEFAULT_RANKING_PARAMS: dict[str, int | float] = {
    "context.max_units": 25,
    "context.relevance_weight": 2.0,
    "context.authority_weight": 1.0,
    "context.token_cost_weight": 1.0,
    "context.duplicate_penalty": 0.0,
}


def rank_units(
    units: list[dict[str, object]],
    task: str,
    budget: int,
    params: dict[str, Any] | None = None,
) -> list[dict[str, object]]:
    settings = {**DEFAULT_RANKING_PARAMS, **(params or {})}
    task_terms = {term.lower() for term in task.replace("-", " ").split() if len(term) > 2}
    scored = []
    signatures: set[tuple[str, str]] = set()
    for unit in units:
        haystack = " ".join([str(unit.get("title", "")), str(unit.get("summary", "")), " ".join(unit.get("tags", []))]).lower()
        relevance = sum(1 for term in task_terms if term in haystack)
        authority = float(unit.get("authority", 0.5))
        tokens = int(unit.get("tokens", 100))
        signature = (str(unit.get("title", "")), str(unit.get("summary", "")))
        duplicate = signature in signatures
        signatures.add(signature)
        score = (
            relevance * float(settings["context.relevance_weight"])
            + authority * float(settings["context.authority_weight"])
            - (float(settings["context.duplicate_penalty"]) if duplicate else 0.0)
        )
        roi = score / max(tokens, 1) ** float(settings["context.token_cost_weight"])
        scored.append((roi, unit, tokens))
    selected = []
    used = 0
    for _, unit, tokens in sorted(scored, key=lambda item: item[0], reverse=True):
        if used + tokens > budget and selected:
            continue
        selected.append(unit)
        used += min(tokens, budget)
        if used >= budget:
            break
    return selected[: int(settings["context.max_units"])]
