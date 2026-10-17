"""Signature and verification tests."""


from typing import Any

from runner.attestation import sign_benchmark, verify_benchmark


def test_sign_and_verify(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    assert "signature" in signed
    assert "cert_hash" in signed
    assert "issuer_pubkey" in signed
    assert verify_benchmark(signed) is True


def test_tamper_detected(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    signed["framework_id"] = "tampered"
    assert verify_benchmark(signed) is False


def test_signature_is_hex_string(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    assert isinstance(signed["signature"], str)
    assert len(signed["signature"]) > 100


def test_cert_hash_is_sha256_hex(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    assert len(signed["cert_hash"]) == 64
    int(signed["cert_hash"], 16)


def test_verify_benchmark_rejects_tampered_signature(sample_benchmark_result: dict[str, Any]) -> None:
    from ube_foundation import PqcKeyPair  # type: ignore[import-untyped]

    key = PqcKeyPair()
    signed = sign_benchmark(sample_benchmark_result, key=key)
    signed["signature"] = "00" * 4627
    assert verify_benchmark(signed, key=key) is False


def test_verify_benchmark_rejects_wrong_key(sample_benchmark_result: dict[str, Any]) -> None:
    from ube_foundation import PqcKeyPair
    signed = sign_benchmark(sample_benchmark_result)
    wrong_key = PqcKeyPair()
    assert verify_benchmark(signed, key=wrong_key) is False


def test_verify_benchmark_rejects_truncated_signature(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    signed["signature"] = signed["signature"][:100]
    assert verify_benchmark(signed) is False


def test_verify_benchmark_rejects_missing_pubkey(sample_benchmark_result: dict[str, Any]) -> None:
    signed = sign_benchmark(sample_benchmark_result)
    del signed["issuer_pubkey"]
    assert verify_benchmark(signed) is False


def test_verify_benchmark_rejects_invalid_inputs() -> None:
    assert verify_benchmark({}) is False
    assert verify_benchmark({"signature": "abc"}) is False
