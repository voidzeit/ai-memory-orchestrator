import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from amo.paths import ai_path


def create_app(repo: Path, require_token: bool = False) -> FastAPI:
    app = FastAPI(title="AMO Server")
    repo = repo.resolve()
    token = os.getenv("AMO_SERVER_TOKEN")

    def check_auth(request: Request) -> None:
        if not require_token:
            return
        supplied = request.query_params.get("token") or request.headers.get("x-amo-token")
        if not token or supplied != token:
            raise HTTPException(status_code=401, detail="Invalid or missing AMO token")

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> str:
        check_auth(request)
        return """
<!doctype html>
<html>
<head><title>AMO Graph</title><style>body{font-family:system-ui;margin:2rem;}pre{background:#111;color:#eee;padding:1rem;overflow:auto;}</style></head>
<body>
<h1>AI Memory Orchestrator</h1>
<p>Local repository memory graph viewer.</p>
<div id="status">Loading graph...</div>
<pre id="graph"></pre>
<script>
fetch('/api/graph' + location.search).then(r => r.json()).then(g => {
  document.getElementById('status').textContent = `${g.nodes?.length || 0} nodes / ${g.edges?.length || 0} edges`;
  document.getElementById('graph').textContent = JSON.stringify(g, null, 2);
});
</script>
</body>
</html>
"""

    @app.get("/api/status")
    def status(request: Request) -> JSONResponse:
        check_auth(request)
        return JSONResponse({"status": "ok", "repo": str(repo)})

    @app.get("/api/graph")
    def graph(request: Request) -> JSONResponse:
        check_auth(request)
        path = ai_path(repo, "machine", "graph.json")
        if not path.exists():
            return JSONResponse({"nodes": [], "edges": [], "warning": "Run amo graph build first."})
        return JSONResponse(content=__import__("json").loads(path.read_text(encoding="utf-8")))

    return app


def serve(repo: Path, host: str, port: int, require_token: bool = False) -> None:
    app = create_app(repo=repo, require_token=require_token)
    uvicorn.run(app, host=host, port=port)
