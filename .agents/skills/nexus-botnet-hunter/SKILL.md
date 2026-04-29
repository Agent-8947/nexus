---
name: nexus-botnet-hunter
description: Autonomous hunter for internal compromised nodes and C2 traffic.
---

## USE FOR
- Analyzing VPC flow logs and proxy traffic for patterns indicating Command & Control (C2) beacons.
- Setting dynamic honeypot listeners inside Kubernetes namespaces.
- Isolating compromised containers without terminating adjacent microservices.

## Instructions
1. **Signal Intelligence:** Beaconing is defined as highly periodic outbound requests with identical payload sizes (+/- 5%) over 24 hours.
2. **Quarantine Logic:** Upon positive ID, apply strict `NetworkPolicies` dropping all egress except to the quarantine analysis node.
3. **Execution Protocol:**
   - [Sniff] Aggregate raw flow logs.
   - [Analyze] Apply FFT algorithms to detect communication periodicity.
   - [Contain] Implement firewall rules dynamically.
4. **Zero-Hallucination Policy:** Do not quarantine critical identity (IdP) nodes. Default to alert-only mode for subnets marked as essential.
