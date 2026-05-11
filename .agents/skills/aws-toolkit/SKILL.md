---
name: aws-toolkit
description: Official AWS Agent Toolkit integration for NEXUS. Provides deep access to AWS services via MCP and curated agent skills. Use when managing AWS infrastructure, deploying services, or analyzing AWS configurations.
when_to_use: Trigger phrases — "aws help", "deploy to aws", "check s3", "configure lambda", "aws infrastructure", "cloud architecture", "aws security", "iam policy", "boto3 help", "aws mcp".
allowed-tools: Bash(python *) Bash(npx *) Read Write Glob Grep
---

# AWS Agent Toolkit for NEXUS

[NEXUS v5.1 — Hardened Integration]

This skill integrates the [AWS Agent Toolkit](https://github.com/aws/agent-toolkit-for-aws) into the NEXUS ecosystem. It enables autonomous cloud engineering through Model Context Protocol (MCP) and structured AWS-specific expertise.

## Core Capabilities

1. **AWS MCP Server Access**: Orchestrates the managed AWS MCP server for real-time API interaction.
2. **Curated Skills Discovery**: Maps AWS-specific tasks to the 50+ specialized skills in the toolkit.
3. **Best Practices Enforcement**: Implements AWS Well-Architected principles and IAM-safe policies.
4. **Sandboxed Execution**: Runs AWS-related Python scripts in isolated environments.

## How to Use

- **Search Skills**: Ask "What AWS skills are available?"
- **Service Specific**: "Help me configure a secure S3 bucket with versioning."
- **Deployment**: "Draft a CloudFormation template for a serverless API."
- **Audit**: "Check my IAM policies for overly permissive permissions."

## Setup Requirement

To activate the full power of this skill, ensure you have:
1. AWS CLI installed and configured (`aws configure`).
2. The AWS MCP Server running (standard port 3000 or via plugin).

## Skill Mapping (Internal)

| Category | Skills Prefix |
| :--- | :--- |
| **Compute** | `aws/compute/` |
| **Storage** | `aws/storage/` |
| **Security** | `aws/security/` |
| **Database** | `aws/database/` |
| **Analytics** | `aws/analytics/` |

---

## NEXUS Workflow: /aws

Use the `/aws` command to initialize an AWS session or search for specific cloud patterns.
