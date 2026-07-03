from amo.core.init import init_repo
from amo.core.validate import validate_repo


def test_validate_returns_status(tmp_path):
    init_repo(tmp_path)
    result = validate_repo(tmp_path)
    assert result["status"] in {"green", "yellow", "red"}
    assert "warnings" in result
