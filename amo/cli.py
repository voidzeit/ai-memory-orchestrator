from pathlib import Path
from typing import Callable, Optional

import typer
from rich.console import Console

from amo.adapters.agents import export_agents_md
from amo.adapters.claude import export_claude_md
from amo.adapters.cline import export_cline_memory_bank
from amo.adapters.cursor import export_cursor_rules
from amo.adapters.opencode import export_opencode_instructions
from amo.config import get_config_value, load_config
from amo.core.context import build_context_pack
from amo.core.benchmark import run_benchmark
from amo.core.evolve import evolve_safe
from amo.core.graph import build_graph, export_graph
from amo.core.handoff import build_handoff
from amo.core.init import init_repo
from amo.core.postflight import apply_postflight
from amo.core.scan import scan_repo
from amo.core.server import serve
from amo.core.status import get_status
from amo.core.validate import validate_repo
from amo.embeddings.index import build_embedding_index, search_embedding_index

app = typer.Typer(help="AI Memory Orchestrator CLI")
graph_app = typer.Typer(help="Graph commands")
obsidian_app = typer.Typer(help="Obsidian adapter commands")
embeddings_app = typer.Typer(help="Embedding index commands")
app.add_typer(graph_app, name="graph")
app.add_typer(obsidian_app, name="obsidian")
app.add_typer(embeddings_app, name="embeddings")
console = Console()

EXPORTERS: dict[str, Callable[[Path], Path]] = {
    "agents": export_agents_md,
    "codex": export_agents_md,
    "claude": export_claude_md,
    "cursor": export_cursor_rules,
    "cline": export_cline_memory_bank,
    "opencode": export_opencode_instructions,
}
LAN_HOSTS = {"0.0.0.0", "::"}


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
    profile: str = typer.Option("", "--profile", "-p"),
    repo: Path = Path("."),
) -> None:
    """Compile token-optimized context for a task."""
    pack = build_context_pack(repo=repo, task=task, profile=profile)
    console.print(f"[green]Context pack generated[/green]: {pack}")


@app.command()
def preflight(
    task: str = typer.Option(..., "--task", "-t", help="Task to prepare context for."),
    profile: str = typer.Option("", "--profile", "-p"),
    repo: Path = Path("."),
) -> None:
    """Generate context before an AI coding session."""
    pack = build_context_pack(repo=repo, task=task, profile=profile)
    console.print(f"[green]Preflight context generated[/green]: {pack}")


@app.command()
def handoff(
    task: str = typer.Option(..., "--task", "-t"),
    summary: str = typer.Option("", "--summary", "-s"),
    repo: Path = Path("."),
) -> None:
    """Create a compact restart pack for long or degraded agent sessions."""
    path = build_handoff(repo=repo, task=task, summary=summary)
    console.print(f"[green]Session handoff generated[/green]: {path}")


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
    if result["status"] == "red":
        raise typer.Exit(code=1)


@app.command()
def status(repo: Path = Path(".")) -> None:
    """Show repository memory status."""
    result = get_status(repo)
    color = "green" if result["status"] == "green" else "yellow"
    console.print(f"[{color}]AMO status: {result['status']}[/{color}]")
    for key, value in result["checks"].items():
        console.print(f"- {key}: {value}")


@app.command()
def server(
    host: Optional[str] = typer.Option(None, "--host"),
    port: Optional[int] = typer.Option(None, "--port"),
    token: bool = False,
    repo: Path = Path("."),
) -> None:
    """Serve the local AMO web graph UI."""
    config = load_config(repo)
    if host is None:
        host = get_config_value(config, "server.host", "127.0.0.1")
    if port is None:
        port = get_config_value(config, "server.port", 8787)
    if host in LAN_HOSTS and not token:
        raise typer.BadParameter("LAN access requires --token. Set AMO_SERVER_TOKEN first.")
    serve(repo=repo, host=host, port=port, require_token=token)


@app.command()
def export(target: str = "agents", repo: Path = Path(".")) -> None:
    """Export AMO instructions to an agent adapter target."""
    if target not in EXPORTERS:
        valid = ", ".join(sorted(EXPORTERS))
        raise typer.BadParameter(f"Unsupported target '{target}'. Valid targets: {valid}")
    path = EXPORTERS[target](repo)
    console.print(f"[green]Exported {target}[/green]: {path}")


@app.command()
def benchmark(
    fixture: Path = typer.Argument(...),
    task: str = typer.Option(..., "--task", "-t"),
) -> None:
    """Measure deterministic context-pack efficiency for a repository fixture."""
    result = run_benchmark(fixture, task)
    console.print(f"[green]Benchmark complete[/green]: {result}")


@app.command()
def evolve(repo: Path = Path(".")) -> None:
    """Record a deterministic, no-LLM memory-quality evolution cycle."""
    result = evolve_safe(repo)
    console.print(f"[green]Safe evolution cycle complete[/green]: {result}")


@graph_app.command("build")
def graph_build(repo: Path = Path(".")) -> None:
    """Build project graph indexes."""
    result = build_graph(repo)
    console.print(f"[green]Graph built[/green]: {result}")


@graph_app.command("export")
def graph_export(
    export_format: str = typer.Option("json", "--format", "-f"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    repo: Path = Path("."),
) -> None:
    """Export the graph as json, jsonld, graphml, gexf, neo4j, or obsidian notes."""
    result = export_graph(repo=repo, export_format=export_format, output=output)
    console.print(f"[green]Graph exported[/green]: {result}")


@embeddings_app.command("build")
def embeddings_build(repo: Path = Path("."), dimensions: int = 128) -> None:
    """Build optional local embedding index from context units."""
    result = build_embedding_index(repo=repo, dimensions=dimensions)
    console.print(f"[green]Embedding index built[/green]: {result}")


@embeddings_app.command("search")
def embeddings_search(
    query: str = typer.Argument(...),
    repo: Path = Path("."),
    top_k: int = typer.Option(5, "--top-k", "-k"),
) -> None:
    """Search optional local embedding index."""
    results = search_embedding_index(repo=repo, query=query, top_k=top_k)
    for item in results:
        console.print(f"{item['score']:.3f}  {item['title']}  -> {item['expand']}")


@obsidian_app.command("sync")
def obsidian_sync(repo: Path = Path("."), path: Optional[Path] = None) -> None:
    """Export AMO memory into Obsidian-compatible Markdown notes."""
    from amo.adapters.obsidian import sync_obsidian

    output = sync_obsidian(repo=repo, output_path=path)
    console.print(f"[green]Obsidian sync complete[/green]: {output}")


if __name__ == "__main__":
    app()
