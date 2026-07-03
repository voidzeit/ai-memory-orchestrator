from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from amo.core.context import build_context_pack
from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.postflight import apply_postflight
from amo.core.scan import scan_repo
from amo.core.server import serve
from amo.core.validate import validate_repo

app = typer.Typer(help="AI Memory Orchestrator CLI")
graph_app = typer.Typer(help="Graph commands")
obsidian_app = typer.Typer(help="Obsidian adapter commands")
app.add_typer(graph_app, name="graph")
app.add_typer(obsidian_app, name="obsidian")
console = Console()


@app.command()
def init(template: str = "generic", repo: Path = Path(".")) -> None:
    """Initialize AMO memory in a repository."""
    result = init_repo(repo=repo, template=template)
    console.print(f"[green]AMO initialized[/green]: {result}")


@app.command()
def scan(repo: Path = Path(".")) -> None:
    """Scan a repository and build machine indexes."""
    result = scan_repo(repo)
    console.print(f"[green]Scan complete[/green]: {result['files_indexed']} files indexed")


@app.command()
def context(
    task: str = typer.Option(..., "--task", "-t", help="Task to compile context for."),
    profile: str = typer.Option("quick", "--profile", "-p"),
    repo: Path = Path("."),
) -> None:
    """Compile token-optimized context for a task."""
    pack = build_context_pack(repo=repo, task=task, profile=profile)
    console.print(f"[green]Context pack generated[/green]: {pack}")


@app.command()
def postflight(
    task: str = typer.Option(..., "--task", "-t"),
    summary: str = typer.Option(..., "--summary", "-s"),
    repo: Path = Path("."),
) -> None:
    """Update memory after a work session."""
    result = apply_postflight(repo=repo, task=task, summary=summary)
    console.print(f"[green]Postflight applied[/green]: {result}")


@app.command()
def validate(repo: Path = Path("."), strict: bool = False) -> None:
    """Validate AMO memory and indexes."""
    result = validate_repo(repo=repo, strict=strict)
    color = "green" if result["status"] == "green" else "yellow"
    console.print(f"[{color}]AMO status: {result['status']}[/{color}]")
    for warning in result["warnings"]:
        console.print(f"[yellow]- {warning}[/yellow]")


@app.command()
def server(host: str = "127.0.0.1", port: int = 8787, token: bool = False, repo: Path = Path(".")) -> None:
    """Serve the local AMO web graph UI."""
    serve(repo=repo, host=host, port=port, require_token=token)


@app.command()
def export(target: str = "agents", repo: Path = Path(".")) -> None:
    """Export AMO instructions to an agent adapter target."""
    if target != "agents":
        raise typer.BadParameter("Only target='agents' is implemented in v0.1 scaffold.")
    from amo.adapters.agents import export_agents_md

    path = export_agents_md(repo)
    console.print(f"[green]Exported[/green]: {path}")


@graph_app.command("build")
def graph_build(repo: Path = Path(".")) -> None:
    """Build project graph indexes."""
    result = build_graph(repo)
    console.print(f"[green]Graph built[/green]: {result}")


@obsidian_app.command("sync")
def obsidian_sync(repo: Path = Path("."), path: Optional[Path] = None) -> None:
    """Export AMO memory into Obsidian-compatible Markdown notes."""
    from amo.adapters.obsidian import sync_obsidian

    output = sync_obsidian(repo=repo, output_path=path)
    console.print(f"[green]Obsidian sync complete[/green]: {output}")


if __name__ == "__main__":
    app()
