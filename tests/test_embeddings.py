from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.embeddings.index import build_embedding_index, search_embedding_index, vectorize


def test_vectorize_is_deterministic():
    assert vectorize("alpha beta gamma") == vectorize("alpha beta gamma")


def test_embedding_index_build_and_search(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "auth.py").write_text("def login(): pass\n", encoding="utf-8")
    scan_repo(tmp_path)
    path = build_embedding_index(tmp_path)
    assert path.exists()
    results = search_embedding_index(tmp_path, "login auth", top_k=3)
    assert len(results) > 0
    assert "score" in results[0]
