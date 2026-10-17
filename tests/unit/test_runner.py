"""Runner tests."""


from pathlib import Path

from benchmarks import ALL_BENCHMARKS
from runner.run_benchmark import run_all, save_results


def test_run_all_includes_every_framework() -> None:
    data = run_all()
    assert data["framework_count"] == len(ALL_BENCHMARKS)
    assert len(data["results"]) == len(ALL_BENCHMARKS)


def test_run_all_has_spec() -> None:
    data = run_all()
    assert data["spec"] == "NTI-Benchmark/1"


def test_run_all_attack_count_positive() -> None:
    data = run_all()
    assert data["attack_count"] >= 5


def test_save_results_creates_file(tmp_path: Path) -> None:
    data = run_all()
    path = save_results(data, str(tmp_path))
    assert path.exists()
