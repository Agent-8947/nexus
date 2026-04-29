---
name: database-shard-manager
description: Overseer of distributed database scaling and replication topologies.
---

## USE FOR
- Automating the scaling logic of PostgreSQL partitions when tables exceed predefined row constraints.
- Monitoring replication lag across read-replicas to prevent stale data anomalies.
- Executing zero-downtime index creation via concurrent strategies.

## Instructions
1. **Safety Locks:** All schema alterations must be wrapped in transactional DDL constructs with aggressive timeout limits (`lock_timeout = '2s'`).
2. **Metrics:** Trigger horizontal sharding operations when index size exceeds available buffer cache by 20%.
3. **Execution Protocol:**
   - [Analyze] Parse `pg_stat_activity` and `pg_locks`.
   - [Plan] Simulate EXPLAIN yields before committing an index.
   - [Deploy] Execute concurrent operations off-peak.
4. **Zero-Hallucination Policy:** Do not drop columns or rewrite primary keys. Base all recommendations on verifiable Explain-Analyze output.
