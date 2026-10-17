"""CLI smoke tests."""


import subprocess
import sys
from pathlib import Path


def test_cli_help() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "--help"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0


def test_cli_verify_invalid_json_returns_error_code_1(tmp_path: Path) -> None:
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("NOT_VALID_JSON{")
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "verify", str(bad_file)],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 1
    assert "INVALID" in r.stdout


def test_cli_verify_nonexistent_file_returns_error() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "verify", "nonexistent_file_path_12345.json"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode != 0




def test_cli_run_subcommand_exists() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "run", "--help"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0




def test_cli_verify_subcommand_exists() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "verify", "--help"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0
