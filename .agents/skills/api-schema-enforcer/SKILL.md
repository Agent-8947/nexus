---
name: api-schema-enforcer
description: Sentinel for REST and GraphQL API contract stability.
---

## USE FOR
- Detecting breaking changes (schema drift) in OpenAPI or GraphQL specifications during CI/CD.
- Validating that incoming request shapes strictly match documented typings.
- Auto-generating test stubs for new endpoint definitions.

## Instructions
1. **Backward Compatibility:** No field removal or type change is allowed unless explicitly mapped to a new `{version}` namespace.
2. **Performance Constraints:** Limit GraphQL depth traversal to a maximum of 5 layers to prevent query DDoS.
3. **Execution Protocol:**
   - [Diff] Compare `main` and feature branch swagger definitions.
   - [Fuzz] Send malformed strings to ensure internal server errors do not leak stack traces.
   - [Block] Hard fail pipeline if a backward-incompatible drift is detected.
4. **Zero-Hallucination Policy:** Only enforce constraints mapped by Swagger/OpenAPI schemas. Do not invent unauthorized API parameters.
