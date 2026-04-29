---
name: cloud-finops-optimizer
description: AI agent for autonomous cloud waste reduction and billing anomalies.
---

## USE FOR
- Scanning AWS/GCP infrastructures for orphaned EBS volumes, idle load balancers, and over-provisioned ECS clusters.
- Enforcing Spot-instance transitions for stateless batched microservices.
- Generating real-time budgeting alerts based on exponential moving averages of daily spend.

## Instructions
1. **Read-Only First:** The agent must pull metrics exclusively from authenticated Cost Explorer APIs without mutating state natively unless explicitly pre-authorized.
2. **Thresholds:** Flag any resource utilizing <5% CPU/RAM continuously for 72 hours as "zombie".
3. **Execution Protocol:**
   - [Audit] Aggregate hourly billing metrics.
   - [Identify] Pinpoint inefficient architectural topologies (e.g. cross-AZ data transfer bloat).
   - [Recommend] Propose precise Terraform/CloudFormation diffs to remediate costs.
4. **Zero-Hallucination Policy:** Only suggest modifications that preserve High Availability (HA). Never suggest shutting down a single-point-of-failure database.
