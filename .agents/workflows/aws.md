# /aws — AWS Agent Toolkit Orchestrator

// turbo-all

This workflow initializes and manages the AWS Agent Toolkit within the NEXUS workspace.

## Phase 0 — Initialization
- Check for AWS CLI: `aws --version`
- Check for NPX: `npx --version`
- Initialize AWS Skills Registry: `npx -y skills add aws/agent-toolkit-for-aws/skills`

## Phase 1 — Context Discovery
- Identify the AWS service in scope (e.g., S3, Lambda, IAM).
- Search for relevant skills in `.agents/skills/aws/`.
- Prompt user for credentials if not detected.

## Phase 2 — Execution
- Load service-specific `SKILL.md`.
- Execute task using `boto3` or `aws-cli` through the MCP server bridge.
- Apply `aws-agent-rules.md` to ensure security compliance.

## Phase 3 — Verification
- Run static analysis on generated CloudFormation/Terraform code.
- Verify resource state via `aws cloudformation describe-stacks` or equivalent.
- Log action to `PROJECT/NEXUS-orchestrator/logs/aws_ops.log`.

---

> [!IMPORTANT]
> **Safety Rule**: Never output raw AWS Access Keys or Secret Keys to the console or logs. Use IAM roles or named profiles.
