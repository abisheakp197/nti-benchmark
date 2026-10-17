"""Run benchmark across all frameworks."""


import json
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from benchmarks import ALL_BENCHMARKS


def run_all(
    progress_cb: Callable[[int, int, str], None] | None = None,
) -> dict[str, Any]:
    results = []
    for i, cls in enumerate(ALL_BENCHMARKS):
        if progress_cb:
            progress_cb(i, len(ALL_BENCHMARKS), cls.framework_name)
        bench = cls()
        results.append(bench.run())


    return {
        "spec": "NTI-Benchmark/1",
        "run_at": datetime.now(UTC).isoformat(),
        "framework_count": len(results),
        "attack_count": results[0]["attack_count"] if results else 0,
        "results": results,
    }




def save_results(data: dict[str, Any], output_dir: str = "results") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = data["run_at"].replace(":", "-").replace(".", "-")
    path = out / f"benchmark-{ts}.json"
    path.write_text(json.dumps(data, indent=2))
    return path
