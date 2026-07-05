from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from amo.core.context import build_context_pack
from amo.core.handoff import build_handoff
from amo.core.postflight import apply_postflight
from amo.core.status import get_status
from amo.io import read_text_if_exists
from amo.paths import ai_path
from amo.server.organism import organism_snapshot

STATIC_DIR = Path(__file__).parent / "static"


class ContextRequest(BaseModel):
    task: str
    profile: str = "quick"


class HandoffRequest(BaseModel):
    task: str
    summary: str = ""


class PostflightRequest(BaseModel):
    task: str
    summary: str
    outcome: str = "completed"
    validation: str = ""
    changed_files: list[str] = []
    decision: str = ""
    confirm: bool = False


def create_app(repo: Path, require_token: bool = False) -> FastAPI:
    app = FastAPI(title="AMO Organism")
    repo = repo.resolve()
    token = os.getenv("AMO_SERVER_TOKEN")

    def check_auth(request: Request) -> None:
        if not require_token:
            return
        supplied = request.query_params.get("token") or request.headers.get("x-amo-token")
        if not token or supplied != token:
            raise HTTPException(status_code=401, detail="Invalid or missing AMO token")

    def machine_json(name: str) -> dict[str, object]:
        path = ai_path(repo, "machine", name)
        if not path.exists():
            raise HTTPException(status_code=404, detail=f"{name} not generated yet")
        return json.loads(path.read_text(encoding="utf-8"))

    @app.get("/", include_in_schema=False)
    def index(request: Request) -> FileResponse:
        check_auth(request)
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/api/status")
    def status(request: Request) -> JSONResponse:
        check_auth(request)
        return JSONResponse(get_status(repo))

    @app.get("/api/organism")
    def organism(request: Request) -> JSONResponse:
        check_auth(request)
        return JSONResponse(organism_snapshot(repo))

    @app.get("/api/graph")
    def graph(request: Request) -> JSONResponse:
        check_auth(request)
        path = ai_path(repo, "machine", "graph.json")
        if not path.exists():
            return JSONResponse({"nodes": [], "edges": [], "warning": "Run amo graph build first."})
        return JSONResponse(json.loads(path.read_text(encoding="utf-8")))

    @app.get("/api/validation")
    def validation(request: Request) -> JSONResponse:
        check_auth(request)
        return JSONResponse(machine_json("validation.json"))

    @app.get("/api/benchmark")
    def benchmark(request: Request) -> JSONResponse:
        check_auth(request)
        return JSONResponse(machine_json("benchmark.json"))

    @app.get("/api/evolution")
    def evolution(request: Request) -> JSONResponse:
        check_auth(request)
        root = repo / ".ai" / "evolution"
        cycles = sorted(root.glob("cycle-*.json"))
        latest = json.loads(cycles[-1].read_text(encoding="utf-8")) if cycles else None
        return JSONResponse(
            {
                "latest_cycle": latest,
                "findings_md": read_text_if_exists(root / "findings.md"),
                "plan_md": read_text_if_exists(root / "plan.md"),
            }
        )

    @app.get("/api/ledger")
    def ledger(request: Request, limit: int = 50) -> JSONResponse:
        check_auth(request)
        from amo.evidence.ledger import read_ledger

        entries = read_ledger(repo)
        return JSONResponse({"total": len(entries), "entries": entries[-limit:]})

    @app.post("/api/context")
    def context(request: Request, body: ContextRequest) -> JSONResponse:
        check_auth(request)
        pack = build_context_pack(repo, task=body.task, profile=body.profile)
        explain_path = ai_path(repo, "machine", "context_explain.json")
        explanation = json.loads(explain_path.read_text(encoding="utf-8")) if explain_path.exists() else None
        return JSONResponse(
            {
                "pack": str(pack.relative_to(repo).as_posix()),
                "content": pack.read_text(encoding="utf-8"),
                "explanation": explanation,
            }
        )

    @app.post("/api/handoff")
    def handoff(request: Request, body: HandoffRequest) -> JSONResponse:
        check_auth(request)
        pack = build_handoff(repo, task=body.task, summary=body.summary)
        return JSONResponse({"handoff": str(pack.relative_to(repo).as_posix())})

    @app.post("/api/postflight")
    def postflight(request: Request, body: PostflightRequest) -> JSONResponse:
        check_auth(request)
        if not body.confirm:
            raise HTTPException(status_code=400, detail="Postflight mutates canonical memory; set confirm=true")
        if not body.summary.strip():
            raise HTTPException(status_code=400, detail="Postflight requires a summary")
        try:
            apply_postflight(
                repo,
                task=body.task,
                summary=body.summary,
                outcome=body.outcome,
                validation=body.validation,
                changed_files=body.changed_files,
                decision=body.decision,
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return JSONResponse({"status": "applied"})

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    return app
