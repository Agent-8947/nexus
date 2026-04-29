---
name: data-lake-governor
description: Automates data lifecycle, partitioning, and cold-storage offloading.
---

## USE FOR
- Migrating structured data older than 90 days from NVMe databases to Amazon S3/Cold storage.
- Ensuring partitioned schemas (`year=YYYY/month=MM`) are continuously updated and balanced.
- Deduplicating redundant event logs across massive distributed queues.

## Instructions
1. **Integrity Rule:** Data transition must employ checksums (`SHA256`) before the primary store is pruned. 
2. **Cost Constraint:** Utilize the cheapest tier of storage (Glacier/Archive) for logs exceeding 365 days.
3. **Execution Protocol:**
   - [Identify] Query timestamp metadata on primary shards.
   - [Move] Stream blocks to object storage with LZ4 compression.
   - [Verify] Re-read random blocks from object storage to ensure readability.
4. **Zero-Hallucination Policy:** Never erase local data if the remote upload checksum fails. Report all byte-mismatches.
