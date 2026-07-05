from pathlib import Path

import uvicorn

from amo.server.app import create_app

__all__ = ["create_app", "serve"]


def serve(repo: Path, host: str, port: int, require_token: bool = False) -> None:
    app = create_app(repo=repo, require_token=require_token)
    uvicorn.run(app, host=host, port=port)
