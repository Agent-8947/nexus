---
name: zero-trust-identity-broker
description: Real-time validator for distributed identity and access management.
---

## USE FOR
- Continuously validating JWT and mTLS credentials across all microservices boundaries.
- Issuing short-lived service tokens dynamically in response to valid CI/CD pipeline triggers.
- Enforcing hardware-key MFA protocols for high-privilege architecture mutating commands.

## Instructions
1. **Token Lifespan:** Maximum TTL for any generated proxy token is strictly 15 minutes. No exceptions.
2. **Session Monitoring:** Instantly revoke tokens if the origin IP or behavioral telemetry changes mid-session.
3. **Execution Protocol:**
   - [Intercept] Evaluate all cross-boundary network requests via sidecar proxy.
   - [Verify] Validate JWKS cryptographic signatures. 
   - [Log] Append authentication decisions to an immutable append-only ledger.
4. **Zero-Hallucination Policy:** Do not grant default permissions. If policy mapping is unclear or missing, the default action is strictly `DENY`.
