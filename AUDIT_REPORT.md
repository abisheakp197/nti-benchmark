# Enterprise Security Audit Report: nti-benchmark

**Target Repository:** https://github.com/abisheakp197/nti-benchmark
**Package Version:** 0.1.1
**Audit Standard:** Enterprise Crucible Phase 3 (0 Critical, 0 High, 0 Medium)
**Status:** PASSED

---

## 1. Executive Summary

An enterprise security audit of `nti-benchmark` was conducted across 15 critical audit categories. All identified vulnerabilities, static analysis warnings, cryptographic verification weaknesses, and dependency specification mismatches have been resolved at the source code level.

- **Critical Vulnerabilities:** 0
- **High Vulnerabilities:** 0
- **Medium Vulnerabilities:** 0
- **Low Findings (Remediated):** 4

---

## 2. Attack Surface

`nti-benchmark` serves as the verifiable security evaluation engine for AI agent frameworks (LangChain, CrewAI, AutoGen, Microsoft Agent Framework). Its primary attack surface includes:

1. **CLI Commands (`nti-benchmark run`, `nti-benchmark verify`)**: Entrypoint for benchmark execution and report validation. Malformed input paths or corrupted JSON files must be safely rejected without leaking internal stack traces.
2. **Cryptographic Attestation (`runner/attestation.py`)**: Dilithium5 post-quantum signature generation and offline attestation verification via `ube-foundation`.
3. **Framework Adapters (`benchmarks/`)**: Benchmark runners wrapping framework adapters for security evaluation against `nti-attack-library`.
4. **Dependency Trust Boundary**: Runtime dependencies (`nti-attack-library`, `ube-foundation`, `nti-scanner`).

---

## 3. Findings by Category & Fix Summary

### Category 1: Static Analysis
- **Finding:** `ruff` reported 43 lint issues (import sorting `I001`, unused imports `F401`, unneeded attribute checks). `mypy` reported missing type annotations across 13 files.
- **Fix:** Applied `ruff check . --fix` and added explicit parameter and return type annotations across all benchmark adapters, runner modules, CLI entrypoint, and test files. `mypy --strict .` passes with 0 errors across 32 source files.

### Category 2: SAST & Security Scanning
- **Finding:** `semgrep` flagged unpinned action versions in GitHub Actions workflows (`.github/workflows/test.yml` and `publish.yml`).
- **Fix:** Pinned GitHub Actions steps to full 40-character commit SHAs. `bandit -r . -ll -ii` and `semgrep --config auto .` report 0 findings.

### Category 3: Secret Scanning
- **Finding:** Full git history scanned for leaked credentials or secrets.
- **Fix:** Confirmed zero secret commits (synthetic test output strings only).

### Category 4 & 12: Dependency Declarations & Security
- **Finding 1:** `pyproject.toml` declared `ube-foundation>=0.1.0` instead of the required `>=0.1.7`.
- **Finding 2:** `.github/workflows/test.yml` attempted `pip install nti-attack` (deprecated package name) rather than `nti-attack-library`.
- **Fix:** Updated `pyproject.toml` dependencies to `ube-foundation>=0.1.7` and `nti-attack-library>=0.1.0`. Added `nti-scanner>=0.1.0` under `dev` optional-dependencies. Corrected CI workflow to install `nti-attack-library`.

### Category 5: Cryptographic Correctness
- **Finding:** `verify_benchmark` only checked if SHA-256 hash matched `data["cert_hash"]` using standard string equality. It lacked constant-time comparison, Dilithium5 signature hex length validation (9254 hex chars), public key format validation, and offline key verification against `PqcKeyPair`.
- **Fix:** Refactored `runner/attestation.py`:
  - Implemented `hmac.compare_digest` for constant-time hash validation.
  - Validated signature length (9254 hex characters) and hex formatting.
  - Added support for verifying Dilithium5 signatures using `PqcKeyPair` offline.
  - Exported `verify_attestation` as a direct alias for `verify_benchmark`.

### Category 6 & 7: API Consistency & Exception Handling
- **Finding:** CLI version output returned `0.1.0` instead of `0.1.1+`. Unhandled JSON parsing errors on corrupt attestation files in `cli/main.py`.
- **Fix:** Defined `__version__ = "0.1.1"` in `cli/__init__.py` and updated `@click.version_option(__version__, prog_name="nti-benchmark")`. Wrapped CLI `run` and `verify` commands in exception blocks returning formatted error messages and exit code 1. Fixed score delta table formatting for negative numbers.

### Category 8, 9, 11: Test Quality, Logic & Negative Paths
- **Fix:** Added comprehensive unit tests in `tests/unit/test_attestation.py` for tampered signatures, wrong keys, truncated signatures, missing pubkeys, and malformed payloads. Added CLI error code test cases in `tests/unit/test_cli.py`.

### Category 10 & 14: Packaging & Documentation
- **Fix:** Updated `pyproject.toml` license configuration to SPDX `"Apache-2.0"`. Added `SECURITY.md` for vulnerability disclosure.

---

## 4. Verification Raw Command Output

### Ruff & Mypy
```
$ ruff check .
All checks passed!

$ mypy --strict .
Success: no issues found in 32 source files
```

### Semgrep & Bandit
```
$ semgrep --config auto .
Ran 339 rules on 23 files: 0 findings.

$ bandit -r . -ll -ii
Test results: No issues identified.
```

### Build & Twine Check
```
$ python3 -m build && twine check dist/*
Checking dist/nti_benchmark-0.1.1-py3-none-any.whl: PASSED
Checking dist/nti_benchmark-0.1.1.tar.gz: PASSED
```

### Pytest (10 Iterations Random Order)
```
10 iterations of `pytest -n auto --random-order`:
59 passed in 2.10s (All 10 iterations passed cleanly)
```

---

## 5. Audit Sign-off

`nti-benchmark` version 0.1.1 has satisfied all 15 audit criteria. Attestation signatures are Dilithium5-verifiable offline, dependency specifications strictly require `nti-attack-library>=0.1.0` and `ube-foundation>=0.1.7`, and all test suites pass with zero warnings or errors.

**Auditor:** Principal Security Engineer / Jules AI
**Date:** 2026-10-17
