from __future__ import annotations

from amo.context.graph_neighborhood import task_terms


def explain_selection(
    selected: list[dict[str, object]],
    task: str,
    proximity: dict[str, float],
    seeds: list[str],
) -> list[dict[str, object]]:
    """Explain why each selected unit made the pack. Deterministic, no LLM."""
    terms = task_terms(task)
    explanations = []
    for unit in selected:
        path = str(unit.get("expand") or unit.get("title") or "")
        haystack = " ".join(
            [str(unit.get("title", "")), str(unit.get("summary", "")), " ".join(unit.get("tags", []))]
        ).lower()
        reasons = []
        if any(term in haystack for term in terms):
            reasons.append("task relevance")
        if path in seeds:
            reasons.append("graph seed")
        elif proximity.get(path, 0.0) > 0.0:
            reasons.append("near selected graph seed")
        if "tests" in unit.get("tags", []):
            reasons.append("is a test")
        authority = float(unit.get("authority", 0.5))
        if authority >= 0.8:
            reasons.append("high authority")
        if not reasons:
            reasons.append("fits remaining token budget")
        explanations.append(
            {
                "path": path,
                "score": unit.get("score"),
                "reasons": reasons,
                "tokens": unit.get("tokens"),
                "authority": authority,
                "graph_proximity": round(proximity.get(path, 0.0), 4),
            }
        )
    return explanations
