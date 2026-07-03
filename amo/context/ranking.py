def rank_units(units: list[dict[str, object]], task: str, budget: int) -> list[dict[str, object]]:
    task_terms = {term.lower() for term in task.replace("-", " ").split() if len(term) > 2}
    scored = []
    for unit in units:
        haystack = " ".join([str(unit.get("title", "")), str(unit.get("summary", "")), " ".join(unit.get("tags", []))]).lower()
        relevance = sum(1 for term in task_terms if term in haystack)
        authority = float(unit.get("authority", 0.5))
        tokens = int(unit.get("tokens", 100))
        score = relevance * 2.0 + authority
        roi = score / max(tokens, 1)
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
    return selected[:25]
