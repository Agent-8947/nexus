---
name: state-anomaly-detector
description: Autonomous system logic monitoring and zero-latency anomaly mitigation agent.
---

## USE FOR
- Real-time continuous analysis of NEXUS ecosystem RAM allocation and CPU spiking behavior.
- Proactive detection of zombie microservices, unbounded loops, and memory leak vectors.
- Automated execution of emergency mitigation protocols (process termination, log rotation, auto-scaling constraints).

## Instructions
1. **Telemetry Ingestion:** Continuously poll `$PROJECT_ROOT/memory.json` and local machine OS-level metrics using native `psutil` or identical system APIs. Do not rely on external cloud telemetry.
2. **Anomaly Thresholds:** 
   - A critical memory spike is defined as sustained usage > 85% for more than 15 seconds.
   - A zombie process is defined as an orphaned child node with stagnant internal state > 60 seconds.
3. **Execution Protocol:** 
   - [Scan] Calculate rolling averages for active nodes. Identify exact PID outliers. 
   - [Verify] Cross-reference against known high-intensity tasks (e.g. video rendering) to prevent false-positive kills.
   - [Act] Execute SIGTERM strictly to flagged PIDs. Log exact termination timestamp and memory reclaimed.
4. **Zero-Hallucination Policy:** Do not invent metrics or terminate processes outside the explicit IDE-NEXUS process tree. Document all diagnostic findings in formal Markdown format within `PROJECT/LOGS/`.
