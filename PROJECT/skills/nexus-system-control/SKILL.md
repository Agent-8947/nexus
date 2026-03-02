---
name: nexus-system-control
description: Manages system health through resource monitoring, bloat cleanup, and performance optimization (Turbo Boost). Use when system lags, high RAM/CPU usage is detected, or when the user requests a health check. Don't use for cloud infrastructure or database migrations.
---

# Nexus System Control

## Overview

This skill provides a centralized suite of tools to maintain local machine performance. It implements the "Turbo Prod" mindset on "Lite Dev" hardware by aggressively reclaiming resources.

## Procedures

### 1. Monitor Resources

To check real-time system health, execute the monitoring script:

```bash
python scripts/monitor.py
```

*Note: This is an interactive terminal session.*

### 2. System Cleanup (Bloat Recovery)

If the system is sluggish due to background apps (Edge, Chrome, Teams, etc.), run the cleanup tool. It uses a predefined list of "bloat" processes in `references/targets.json`.

```bash
python scripts/clean_bloat.py
```

### 3. Ultimate Turbo Boost

For maximum performance during heavy tasks (compilation, training), trigger the Turbo Boost. It compresses memory working sets and clears temporary caches.

```bash
python scripts/turbo_boost.py
```

### 4. Alerting

Send status updates to the administrator via Telegram:

```bash
python scripts/notify.py --message "System Optimized"
```

## References

- `references/targets.json`: List of processes to kill and paths to clean.
- `references/system_info.md`: Hardware baseline and optimization logs.

## Error Handling

- **Admin Rights**: Cleanup and Turbo scripts may fail to touch system processes without elevation. Notify the user to "Run as Admin" if access is denied.
- **Visual Safety**: The scripts avoid killing IDEs or active development windows unless explicitly added to `targets.json`.
