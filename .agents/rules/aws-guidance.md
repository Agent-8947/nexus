# AWS Agent Rules (NEXUS Integration)

[Source: https://github.com/aws/agent-toolkit-for-aws/blob/main/rules/aws-agent-rules.md]

- **Prefer the AWS MCP Server** for AWS interactions — it provides sandboxed execution, observability, and audit logging. If unavailable, use the AWS CLI directly.
- **Before starting a task, check whether a relevant AWS skill is available**. Load the skill and prefer its guidance over general knowledge.
- **When uncertain about specific AWS details** (API parameters, permissions, limits, error codes), verify against documentation rather than guessing. State uncertainty explicitly if you cannot confirm.
- **When creating infrastructure, prefer infrastructure-as-code** (AWS CDK or CloudFormation) over direct CLI commands.
- **When working with infrastructure, follow AWS Well-Architected Framework principles**.
- **Security First**: Never hardcode credentials. Use IAM roles, environment variables, or named profiles.
- **Observability**: Log all AWS operations to `PROJECT/NEXUS-orchestrator/logs/aws_ops.log`.
