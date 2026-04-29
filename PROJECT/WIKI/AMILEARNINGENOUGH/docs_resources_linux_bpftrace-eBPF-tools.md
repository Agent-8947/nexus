# BPFtrace and eBPF Tools Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Layer Overview](#system-layer-overview)
3. [Tool Categories](#tool-categories)
4. [Detailed Tool Analysis](#detailed-tool-analysis)
5. [Command Reference](#command-reference)

## Introduction

This guide covers the comprehensive set of bpftrace and eBPF tools available for Linux system analysis and performance monitoring across different layers of the system stack.

## System Layer Overview

The tools are organized across these main layers:
1. Applications & Runtimes
2. System Libraries
3. System Call Interface
4. Kernel Subsystems:
   - VFS (Virtual File System)
   - Network Stack (Sockets, TCP/UDP, IP)
   - Scheduler
   - Virtual Memory
   - Device Drivers

## Tool Categories

### Application Level Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| opensnoop | Trace file opens | Application |
| statsnoop | Trace stat() syscalls | Application |
| syncsnoop | Trace sync operations | Application |
| bashreadline | Trace bash commands | Application |
| gethostlatency | DNS latency analysis | System Libraries |

### System Call Interface Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| syscount | Count syscalls | System Call |
| execsnoop | Trace new processes | System Call |
| killsnoop | Trace kill() syscalls | System Call |
| pidpersec | New processes per second | System Call |

### File System Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| vfscount | VFS operation counts | VFS |
| vfsstat | VFS operation stats | VFS |
| writeback | Trace file writeback | File Systems |
| xfsdist | XFS operation latency | File Systems |
| mdflush | Trace md RAID flush events | Volume Manager |

### Block Device Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| biosnoop | Trace block I/O | Block Device |
| biolatency | Block I/O latency | Block Device |
| bitesize | Block I/O size analysis | Block Device |

### Network Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| tcpconnect | Trace TCP connections | TCP/UDP |
| tcpaccept | Trace TCP accepts | TCP/UDP |
| tcpretrans | Trace TCP retransmits | TCP/UDP |
| tcpdrop | Trace TCP drops | TCP/UDP |

### CPU/Scheduler Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| cpuwalk | CPU instruction analysis | Scheduler |
| runqlat | Run queue latency | Scheduler |
| runqlen | Run queue length | Scheduler |
| offcputime | Off-CPU analysis | Scheduler |

### Memory Management Tools
| Tool | Purpose | Layer |
|------|---------|-------|
| oomkill | Trace OOM killer | Virtual Memory |
| capable | Trace capability checks | System |

## Detailed Tool Analysis

### Application Monitoring Tools

#### opensnoop
```bash
# Trace all file opens
opensnoop

# Trace specific process
opensnoop -p 1234

# Include stack traces
opensnoop --stack

# Filter by file name
opensnoop -n "*.txt"
```

#### statsnoop
```bash
# Trace all stat() calls
statsnoop

# Show failed stats only
statsnoop -x

# Filter by process name
statsnoop -n "nginx"

# Include extended details
statsnoop -v
```

#### bashreadline
```bash
# Trace all bash commands
bashreadline

# Include timestamps
bashreadline -t

# Trace specific shell PID
bashreadline -p 1234
```

### Network Analysis Tools

#### tcpconnect
```bash
# Trace all TCP connections
tcpconnect

# Show port numbers
tcpconnect -p

# Include timestamps
tcpconnect -t

# Filter by port
tcpconnect -P 80
```

#### tcpretrans
```bash
# Trace TCP retransmissions
tcpretrans

# Include TCP state
tcpretrans -s

# Show stack traces
tcpretrans --stack

# Filter by IP
tcpretrans -i 192.168.1.1
```

### File System Analysis

#### vfscount
```bash
# Count VFS operations
vfscount

# Group by operation type
vfscount -g

# Include stack traces
vfscount --stack
```

#### writeback
```bash
# Trace file writeback
writeback

# Show per-device stats
writeback -d

# Include process info
writeback -p
```

### Block Device Analysis

#### biosnoop
```bash
# Trace block I/O
biosnoop

# Show queued time
biosnoop -q

# Filter by device
biosnoop -d sda

# Include process info
biosnoop -p
```

#### biolatency
```bash
# Show block I/O latency
biolatency

# Use microsecond units
biolatency -u

# Create histogram
biolatency -h

# Filter by device
biolatency -d sda
```

### CPU and Scheduler Analysis

#### runqlat
```bash
# Show run queue latency
runqlat

# Use microsecond units
runqlat -u

# Filter by CPU
runqlat -c 0

# Create histogram
runqlat --hist
```

#### offcputime
```bash
# Trace off-CPU time
offcputime

# Filter by process
offcputime -p 1234

# Set duration
offcputime -d 10

# Include user stacks
offcputime -u
```

## Command Reference

### General Options
Most bpftrace tools support these common options:
```bash
-h          # Show help message
-v          # Verbose output
-d          # Debug output
-p PID      # Filter by process ID
-t          # Include timestamps
--stack     # Show stack traces
```

### Advanced Usage

#### Custom Scripts
```bash
# Create custom bpftrace script
cat > custom.bt << 'EOF'
#!/usr/bin/bpftrace
tracepoint:syscalls:sys_enter_open
{
    printf("%s opened %s\n", comm, str(args->filename));
}
EOF

# Run custom script
bpftrace custom.bt
```

#### Performance Monitoring
```bash
# Monitor system calls
syscount -i 1

# Monitor process creation
pidpersec -i 5

# Track OOM kills
oomkill -t
```

### Best Practices

1. **Resource Usage**
   - Be cautious with stack traces in production
   - Use sampling for high-frequency events
   - Monitor overhead with top/htop

2. **Filtering**
   - Use specific filters to reduce overhead
   - Combine multiple conditions when possible
   - Consider using time-based filters

3. **Output Control**
   - Use appropriate output formats
   - Consider logging to files for analysis
   - Use aggregation for high-volume data

4. **Troubleshooting**
   - Start with broad tools
   - Narrow down to specific events
   - Use multiple tools for correlation

## Performance Considerations

### Overhead Management
```bash
# Reduce overhead with sampling
biolatency --sample-rate 10

# Use efficient filters
opensnoop -n '*.log'

# Limit stack traces
tcpconnect --stack --stack-storage-size 1024
```

### Production Usage
1. Test tools in development first
2. Use appropriate filtering
3. Monitor system impact
4. Set appropriate buffer sizes
5. Use time-based execution limits

## Common Use Cases

### Performance Analysis
```bash
# Analyze disk I/O
biolatency -h
biosnoop -p

# Network performance
tcpretrans -s
tcpconnect -t

# CPU scheduling
runqlat --hist
offcputime -p 1234
```

### Troubleshooting
```bash
# File system issues
opensnoop -t
vfscount

# Network problems
tcpdrop
tcpretrans

# Memory issues
oomkill -t
```

### Security Monitoring
```bash
# Track capability checks
capable -v

# Monitor process creation
execsnoop -t

# Track file access
opensnoop -t
```
