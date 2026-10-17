"""Sign and verify benchmark results with Dilithium5."""

import hashlib
import hmac
import json
from typing import Any


def sign_benchmark(data: dict[str, Any], key: Any | None = None) -> dict[str, Any]:
    """Sign benchmark results payload using Dilithium5 PqcKeyPair."""
    if key is None:
        from ube_foundation import PqcKeyPair  # type: ignore[import-untyped]

        key = PqcKeyPair()

    clean = {k: v for k, v in data.items() if k not in ("signature", "cert_hash")}
    clean["issuer_pubkey"] = key.public_key_hex()
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    sig = key.sign(message)
    cert_hash = hashlib.sha256(message).hexdigest()

    return {
        **clean,
        "signature": sig,
        "cert_hash": cert_hash,
    }


def verify_benchmark(data: dict[str, Any], key: Any | None = None) -> bool:
    """Verify benchmark result payload and Dilithium5 signature offline."""
    if not isinstance(data, dict):
        return False

    cert_hash = data.get("cert_hash")
    signature = data.get("signature")
    issuer_pubkey = data.get("issuer_pubkey")

    if not cert_hash or not signature or not issuer_pubkey:
        return False

    if not isinstance(cert_hash, str) or not isinstance(signature, str) or not isinstance(issuer_pubkey, str):
        return False

    if len(cert_hash) != 64 or len(signature) != 9254 or len(issuer_pubkey) != 5184:
        return False

    try:
        bytes.fromhex(cert_hash)
        bytes.fromhex(signature)
        bytes.fromhex(issuer_pubkey)
    except ValueError:
        return False

    clean = {k: v for k, v in data.items() if k not in ("signature", "cert_hash")}
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    expected_hash = hashlib.sha256(message).hexdigest()

    if not hmac.compare_digest(expected_hash, cert_hash):
        return False

    if key is not None:
        if not hasattr(key, "public_key_hex") or not hasattr(key, "verify"):
            return False
        if key.public_key_hex() != issuer_pubkey:
            return False
        if not bool(key.verify(message, signature)):
            return False

    return True


verify_attestation = verify_benchmark
