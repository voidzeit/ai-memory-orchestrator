from amo.core.scan import normalize_excludes


def test_normalize_excludes_handles_string():
    assert normalize_excludes("dist") == {"dist"}


def test_normalize_excludes_handles_list():
    assert normalize_excludes(["dist", "build"]) == {"dist", "build"}


def test_normalize_excludes_rejects_invalid_type():
    assert normalize_excludes({"bad": "value"}) == set()
