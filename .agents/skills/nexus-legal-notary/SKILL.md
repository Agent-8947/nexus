---
name: nexus-legal-notary
description: Automated compliance checker for Legal DevOps workflows.
---

## USE FOR
- Ensuring generated code, logs, and processes comply with GDPR, CCPA, and SOC2 regulations.
- Automating cryptographic timestamping of critical Git commits to provide legal non-repudiation.
- Redacting PII (Personally Identifiable Information) from application traces before long-term storage.

## Instructions
1. **Regex Strictness:** Employ standard global PII patterns for credit cards, SSN, and localized IDs.
2. **Compliance Verification:** Block any database migration script that drops audit trails or modifies immutable transaction ledgers.
3. **Execution Protocol:**
   - [Ingest] Scan pull requests for data collection changes.
   - [Notarize] Validate digital signatures of the developer asserting the change.
   - [Enforce] Reject code lacking necessary "Privacy Policy Updated" flags.
4. **Zero-Hallucination Policy:** Only enforce constraints dictated in `PROJECT/CONSTITUTION.md`. Do not invent new legal frameworks.
