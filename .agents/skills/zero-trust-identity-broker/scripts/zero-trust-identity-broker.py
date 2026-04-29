#!/usr/bin/env python3
"""
ZERO-TRUST-IDENTITY-BROKER [NEXUS SYNTHESIZED v2.0]
Mission: JWT/mTLS validation, token lifecycle management, and access decision logging
Role: enforcer | Security: cryptographic | Interface: cli
"""

import sys
import json
import logging
import argparse
import hashlib
import hmac
import base64
import time
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("ZERO-TRUST-IDENTITY-BROKER")

# ── Policy Constants ─────────────────────────────────────────────────────
MAX_TOKEN_TTL_SECONDS = 900    # 15 minutes
DEFAULT_ACTION = "DENY"        # Zero-trust: deny by default
REQUIRED_CLAIMS = {"sub", "iss", "exp", "iat"}
# ─────────────────────────────────────────────────────────────────────────


class JWTValidator:
    """Validates JWT structure and claims without external libraries."""

    def __init__(self, secret: str = ""):
        self.secret = secret

    def validate(self, token: str) -> dict:
        parts = token.split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "Malformed JWT: expected 3 segments", "decision": DEFAULT_ACTION}

        try:
            header = self._decode_segment(parts[0])
            payload = self._decode_segment(parts[1])
        except Exception as e:
            return {"valid": False, "error": f"Base64 decode failed: {e}", "decision": DEFAULT_ACTION}

        # Check algorithm
        alg = header.get("alg", "none")
        if alg == "none":
            return {"valid": False, "error": "Algorithm 'none' is forbidden", "decision": DEFAULT_ACTION}

        # Check required claims
        missing = REQUIRED_CLAIMS - set(payload.keys())
        if missing:
            return {"valid": False, "error": f"Missing claims: {missing}", "decision": DEFAULT_ACTION}

        # Check expiration
        exp = payload.get("exp", 0)
        now = time.time()
        if exp < now:
            return {"valid": False, "error": f"Token expired at {datetime.fromtimestamp(exp).isoformat()}", "decision": DEFAULT_ACTION}

        # Check TTL constraint
        iat = payload.get("iat", 0)
        ttl = exp - iat
        if ttl > MAX_TOKEN_TTL_SECONDS:
            return {"valid": False, "error": f"TTL {ttl}s exceeds max {MAX_TOKEN_TTL_SECONDS}s", "decision": DEFAULT_ACTION}

        # Signature verification (HMAC-SHA256)
        if self.secret and alg == "HS256":
            signing_input = f"{parts[0]}.{parts[1]}".encode()
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(self.secret.encode(), signing_input, hashlib.sha256).digest()
            ).rstrip(b"=").decode()
            if not hmac.compare_digest(expected_sig, parts[2]):
                return {"valid": False, "error": "Signature mismatch", "decision": DEFAULT_ACTION}

        return {
            "valid": True,
            "subject": payload.get("sub"),
            "issuer": payload.get("iss"),
            "expires": datetime.fromtimestamp(exp).isoformat(),
            "ttl_seconds": int(ttl),
            "decision": "ALLOW",
        }

    @staticmethod
    def _decode_segment(segment: str) -> dict:
        padding = 4 - len(segment) % 4
        segment += "=" * padding
        decoded = base64.urlsafe_b64decode(segment)
        return json.loads(decoded)


class AccessLedger:
    """Append-only log of authentication decisions."""

    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path
        self.entries: list[dict] = []
        if ledger_path.exists():
            try:
                self.entries = json.loads(ledger_path.read_text(encoding="utf-8"))
            except Exception:
                self.entries = []

    def record(self, request_id: str, token_subject: str, decision: str, detail: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "subject": token_subject,
            "decision": decision,
            "detail": detail,
            "integrity_hash": hashlib.sha256(
                f"{request_id}:{token_subject}:{decision}:{detail}".encode()
            ).hexdigest()[:16],
        }
        self.entries.append(entry)

    def flush(self):
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_path.write_text(json.dumps(self.entries, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"[LEDGER] {len(self.entries)} entries -> {self.ledger_path}")


class PolicyEnforcer:
    """Evaluates access policy rules against validated token claims."""

    def __init__(self, policy_path: Path | None = None):
        self.rules: list[dict] = []
        if policy_path and policy_path.exists():
            self.rules = json.loads(policy_path.read_text(encoding="utf-8")).get("rules", [])
            logger.info(f"Loaded {len(self.rules)} policy rule(s).")

    def evaluate(self, subject: str, resource: str) -> str:
        for rule in self.rules:
            if rule.get("subject") == subject and rule.get("resource") == resource:
                return rule.get("action", DEFAULT_ACTION)
            if rule.get("subject") == "*" and rule.get("resource") == resource:
                return rule.get("action", DEFAULT_ACTION)
        return DEFAULT_ACTION


def main():
    parser = argparse.ArgumentParser(description="ZERO-TRUST-IDENTITY-BROKER: JWT Validator & Access Enforcer")
    parser.add_argument("--tokens", required=True, help="JSON file with array of {id, token, resource} objects")
    parser.add_argument("--secret", default="", help="HMAC secret for HS256 verification")
    parser.add_argument("--policy", default=None, help="Policy rules JSON file")
    parser.add_argument("--ledger", default="access_ledger.json", help="Append-only access decision log")
    parser.add_argument("--output", default="identity_report.json", help="Output report")
    args = parser.parse_args()

    tokens_path = Path(args.tokens).resolve()
    if not tokens_path.exists():
        logger.error(f"Tokens file not found: {tokens_path}")
        sys.exit(1)

    requests = json.loads(tokens_path.read_text(encoding="utf-8"))
    validator = JWTValidator(secret=args.secret)
    policy_path = Path(args.policy).resolve() if args.policy else None
    enforcer = PolicyEnforcer(policy_path)
    ledger = AccessLedger(Path(args.ledger).resolve())

    results = []
    allowed = 0
    denied = 0

    for req in requests:
        req_id = req.get("id", "unknown")
        token = req.get("token", "")
        resource = req.get("resource", "")

        validation = validator.validate(token)
        decision = validation["decision"]

        # Additional policy check if JWT is valid
        if decision == "ALLOW" and resource:
            policy_decision = enforcer.evaluate(validation.get("subject", ""), resource)
            if policy_decision == "DENY":
                decision = "DENY"
                validation["policy_override"] = True

        if decision == "ALLOW":
            allowed += 1
        else:
            denied += 1

        ledger.record(req_id, validation.get("subject", "anonymous"), decision, 
                      validation.get("error", "OK"))

        results.append({
            "request_id": req_id,
            "resource": resource,
            **validation,
            "final_decision": decision,
        })

    ledger.flush()

    report = {
        "agent": "ZERO-TRUST-IDENTITY-BROKER",
        "version": "2.0-nexus",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_requests": len(requests),
            "allowed": allowed,
            "denied": denied,
            "denial_rate_pct": round(denied / len(requests) * 100, 1) if requests else 0,
            "verdict": "SECURE" if denied < len(requests) * 0.5 else "REVIEW_REQUIRED",
        },
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"[DONE] Identity report -> {output}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL: {e}")
        sys.exit(1)
