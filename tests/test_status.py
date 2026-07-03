from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.core.graph import build_graph
from amo.core.status import get_status
from amo.core.validate import validate_repo


def test_status_reports_memory_checks(tmp_path):
    init_repo(tmp_path)
    scan_repo(tmp_path)
    build_graph(tmp_path)
    validate_repo(tmp_path)
    result = get_status(tmp_path)
    assert result["status"] == "green"
    assert result["checks"]["memory"] == "ok"
    assert result["checks"]["graph"] == "ok"
