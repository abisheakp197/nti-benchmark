"""Command-line interface for nti-benchmark."""


import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli import __version__
from runner.attestation import sign_benchmark, verify_benchmark
from runner.run_benchmark import run_all, save_results

console = Console()


@click.group()
@click.version_option(__version__, prog_name="nti-benchmark")
def main() -> None:
    """nti-benchmark: verifiable security benchmark for AI agent frameworks."""


@main.command()
@click.option("--output", "-o", default="results", help="Output directory")
@click.option("--sign/--no-sign", default=True, help="Sign results with Dilithium5")
def run(output: str, sign: bool) -> None:
    """Run the benchmark across all frameworks."""
    console.print("[bold cyan]Running NTI Benchmark...[/bold cyan]\n")

    def progress(i: int, total: int, name: str) -> None:
        console.print(f"[{i+1}/{total}] Running: {name}")

    try:
        data = run_all(progress_cb=progress)

        if sign:
            data = sign_benchmark(data)

        path = save_results(data, output)

        table = Table(title="NTI Benchmark Results")
        table.add_column("Framework", style="cyan")
        table.add_column("Bare Score", justify="right")
        table.add_column("With NTI", justify="right")
        table.add_column("Delta", justify="right")

        for r in data["results"]:
            delta = r["delta"]
            delta_str = f"+{delta}" if delta >= 0 else f"{delta}"
            delta_color = "green" if delta > 0 else "red"
            table.add_row(
                r["framework_name"],
                f"{r['bare']['score']}/100",
                f"[green]{r['with_nti']['score']}/100[/green]",
                f"[{delta_color}]{delta_str}[/{delta_color}]",
            )

        console.print()
        console.print(table)
        console.print()
        console.print(f"Report saved: {path}")
        if sign:
            console.print("[green]Signed with Dilithium5[/green]")
    except (RuntimeError, OSError, ValueError) as e:
        console.print(f"[bold red]Error running benchmark:[/bold red] {e}")
        sys.exit(1)


@main.command()
@click.argument("path", type=click.Path(exists=True))
def verify(path: str) -> None:
    """Verify a signed benchmark report offline."""
    try:
        content = Path(path).read_text(encoding="utf-8")
        data = json.loads(content)
        if verify_benchmark(data):
            console.print(Panel.fit("[green]VALID[/green]", title="Verification"))
        else:
            console.print(Panel.fit("[red]INVALID[/red]", title="Verification"))
            sys.exit(1)
    except (json.JSONDecodeError, FileNotFoundError, OSError, ValueError) as e:
        console.print(Panel.fit(f"[red]INVALID (Error: {e})[/red]", title="Verification"))
        sys.exit(1)




if __name__ == "__main__":
    main()
