# Duties

## Roles

| Role | Agent | Permissions | Description |
|------|-------|-------------|-------------|
| Maker | [Agent Name] | create, edit | Generates content or code |
| Checker | [Agent Name/User] | review, approve | Validates for errors/risk |
| Auditor | [Agent Name] | log, report | Maintains immutable audit trail |

## Conflict Matrix
- **Maker <-> Checker**: One agent cannot approve its own work.
- **Checker <-> Auditor**: The reviewer cannot be the final auditor.

## Handoff Workflows
### [Example: Code Deployment]
1. **Maker** creates the PR.
2. **Checker** runs security-audit and approves.
3. User triggers the final deploy.

## Enforcement
Mode: **strict**
Any violation blocks the execution flow.
