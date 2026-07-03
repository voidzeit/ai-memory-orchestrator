from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

from amo.io import write_json, write_text
from amo.paths import ai_path

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]{3,}")
DEFAULT_DIMENSIONS = 128


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def vectorize(text: str, dimensions: int = DEFAULT_DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b))


def build_embedding_index(repo: Path, dimensions: int = DEFAULT_DIMENSIONS) -> Path:
    repo = repo.resolve()
    units_path = ai_path(repo, "machine", "context_units.json")
    if not units_path.exists():
        raise FileNotFoundError("Run `amo scan` before building embeddings.")
    units = json.loads(units_path.read_text(encoding="utf-8")).get("units", [])
    rows = []
    for unit in units:
        text = " ".join([str(unit.get("title", "")), str(unit.get("summary", "")), " ".join(unit.get("tags", []))])
        rows.append(
            {
                "id": unit["id"],
                "title": unit.get("title"),
                "type": unit.get("type"),
                "expand": unit.get("expand"),
                "dimensions": dimensions,
                "vector": vectorize(text, dimensions=dimensions),
            }
        )
    index_path = ai_path(repo, "machine", "embedding_index.json")
    write_json(index_path, {"schema_version": "0.1", "provider": "amo-local-hash", "dimensions": dimensions, "items": rows})
    jsonl_path = ai_path(repo, "machine", "embeddings.jsonl")
    write_text(jsonl_path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    return index_path


def search_embedding_index(repo: Path, query: str, top_k: int = 5) -> list[dict[str, object]]:
    repo = repo.resolve()
    index_path = ai_path(repo, "machine", "embedding_index.json")
    if not index_path.exists():
        raise FileNotFoundError("Run `amo embeddings build` before searching embeddings.")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    query_vector = vectorize(query, dimensions=int(index.get("dimensions", DEFAULT_DIMENSIONS)))
    results = []
    for item in index.get("items", []):
        score = cosine(query_vector, item.get("vector", []))
        results.append({"score": score, "id": item.get("id"), "title": item.get("title"), "expand": item.get("expand")})
    return sorted(results, key=lambda item: float(item["score"]), reverse=True)[:top_k]
