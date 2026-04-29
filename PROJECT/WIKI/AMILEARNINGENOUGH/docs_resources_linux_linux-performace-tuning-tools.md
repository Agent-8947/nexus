# Linux Performance Tuning Tools Cheatlist

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture Overview](#system-architecture-overview)
3. [Performance Tool Categories](#performance-tool-categories)
4. [Detailed Tool Analysis](#detailed-tool-analysis)
5. [Command Cheatsheet](#command-cheatsheet)

## Introduction

This comprehensive guide covers Linux performance analysis and tuning tools across different layers of the operating system stack, from applications to hardware. The tools are organized based on their operational layer and specific functionality.

## System Architecture Overview

The Linux system architecture consists of several layers:

1. Application Layer
2. System Libraries
3. System Call Interface
4. Kernel Space
   - VFS (Virtual File System)
   - Network Stack
   - Scheduler
   - Device Drivers
5. Hardware Layer

## Performance Tool Categories

### Application Level Tools

| Tool | Layer | Purpose |
|------|-------|---------|
| App Config | Application | Application configuration management |
| env | System Libraries | Environment variable management |
| tune2fs | File System | File system parameters tuning |

### System Level Tools

| Tool | Layer | Purpose |
|------|-------|---------|
| nice/renice | Scheduler | Process priority adjustment |
| taskset | CPU Management | CPU affinity control |
| ulimit | Resource Control | Resource limits management |
| sysctl | Kernel Parameters | Kernel parameter tuning |

### Kernel Level Tools

| Tool | Layer | Purpose |
|------|-------|---------|
| stap | Kernel Tracing | SystemTap scripts for kernel analysis |
| kpatch | Kernel Patching | Live kernel patching |
| ionice | I/O Scheduling | I/O priority management |
| MegaCli | Storage Management | RAID controller management |

### Network Tools

| Tool | Layer | Purpose |
|------|-------|---------|
| ip route | Network Stack | IP routing table management |
| tc | Traffic Control | Network traffic control |
| ethtool | Network Driver | Network interface configuration |

### Storage Tools

| Tool | Layer | Purpose |
|------|-------|---------|
| hdparm | Disk Management | Hard drive parameter management |
| blockdev | Block Devices | Block device management |
| swapon | Memory Management | Swap space control |

## Detailed Tool Analysis

### System Control Tools

#### sysctl
```bash
# View all system parameters
sysctl -a

# Set a specific parameter
sysctl -w vm.swappiness=60

# Load settings from file
sysctl -p /etc/sysctl.conf

# Common parameters
sysctl kernel.pid_max=4194304
sysctl vm.max_map_count=262144
sysctl net.ipv4.tcp_wmem="4096 87380 16777216"
```

#### nice/renice
```bash
# Start a process with specific priority (-20 to 19)
nice -n 10 ./myprocess

# Change priority of running process
renice -n 5 -p PID

# Change priority for all processes of a user
renice -n 3 -u username

# Change priority for process group
renice -n 7 -g process_group
```

#### taskset
```bash
# Launch process on specific CPU
taskset -c 0 ./myprocess

# Move running process to specific CPU
taskset -pc 1 PID

# View process CPU affinity
taskset -p PID

# Set CPU affinity using mask
taskset 0x01 ./myprocess
```

### Storage Management Tools

#### ionice
```bash
# Set I/O scheduling class and priority
ionice -c 2 -n 0 -p PID

# Run command with best-effort scheduling
ionice -c 2 -n 0 command

# View process I/O scheduling
ionice -p PID

# Set real-time I/O priority
ionice -c 1 -n 0 command
```

#### hdparm
```bash
# Get drive parameters
hdparm -I /dev/sda

# Set drive performance parameters
hdparm -d1 -A1 -m16 -u1 -a64 /dev/sda

# Perform drive speed test
hdparm -tT /dev/sda

# Enable/disable drive caching
hdparm -W1 /dev/sda
```

#### blockdev
```bash
# Get device parameters
blockdev --getsize64 /dev/sda

# Set read-ahead buffer
blockdev --setra 4096 /dev/sda

# Flush device buffers
blockdev --flushbufs /dev/sda

# Set device read-only
blockdev --setro /dev/sda
```

### Network Management Tools

#### ethtool
```bash
# View interface settings
ethtool eth0

# Set interface speed and duplex
ethtool -s eth0 speed 1000 duplex full

# Show interface statistics
ethtool -S eth0

# Set rx/tx ring parameters
ethtool -G eth0 rx 4096 tx 4096

# Enable/disable features
ethtool -K eth0 tso on gso on gro on
```

#### tc (Traffic Control)
```bash
# Add traffic shaping rule
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms

# Show queueing disciplines
tc qdisc show dev eth0

# Add classification rule
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 192.168.1.0/24 flowid 1:1

# Delete all traffic rules
tc qdisc del dev eth0 root
```

#### ip route
```bash
# Show routing table
ip route show

# Add static route
ip route add 192.168.2.0/24 via 192.168.1.1

# Add route with metric
ip route add default via 192.168.1.1 metric 100

# Delete route
ip route del 192.168.2.0/24
```

### Memory Management Tools

#### numactls
```bash
# Show NUMA topology
numactl --hardware

# Run process on specific node
numactl --membind=0 --cpunodebind=0 command

# Show NUMA statistics
numactl --show

# Set NUMA policy
numactl --interleave=all command
```

#### swapon/swapoff
```bash
# Enable swap file/partition
swapon /swapfile

# Disable swap
swapoff -a

# Show swap usage
swapon --show

# Set swap priority
swapon -p 1 /dev/sda2
```

### Kernel Tracing Tools

#### SystemTap (stap)
```bash
# Compile and run SystemTap script
stap script.stp

# List available probe points
stap -l 'kernel.function("*")'

# Create kernel module
stap -p4 script.stp

# Run with verbose output
stap -v script.stp

# Example SystemTap script for syscall tracing
cat << EOF > syscall_trace.stp
probe syscall.* {
  printf("%s(%d) syscall: %s\n",
         execname(), pid(), name)
}
EOF
stap syscall_trace.stp
```

#### kpatch
```bash
# List active patches
kpatch list

# Apply kernel patch
kpatch load patch.ko

# Remove kernel patch
kpatch unload patch.ko

# Enable automatic loading
kpatch enable patch.ko
```

### File System Tools

#### tune2fs
```bash
# Show filesystem information
tune2fs -l /dev/sda1

# Change filesystem parameters
tune2fs -c 30 -i 60d /dev/sda1

# Enable/disable filesystem features
tune2fs -O has_journal,extent /dev/sda1

# Set filesystem label
tune2fs -L "ROOT_FS" /dev/sda1
```

## Command Cheatsheet

### System Analysis

| Command | Purpose | Common Usage |
|---------|---------|--------------|
| `top` | Process monitoring | `top -b -n 1` |
| `htop` | Interactive process viewer | `htop -d 10` |
| `vmstat` | Virtual memory statistics | `vmstat 1 10` |
| `iostat` | I/O statistics | `iostat -xz 1` |
| `mpstat` | CPU statistics | `mpstat -P ALL 1` |
| `sar` | System activity reporter | `sar -n DEV 1` |

### Resource Limits

| Command | Purpose | Example |
|---------|---------|---------|
| `ulimit -n` | File descriptor limit | `ulimit -n 65535` |
| `ulimit -u` | Process limit | `ulimit -u 16384` |
| `ulimit -m` | Memory limit | `ulimit -m unlimited` |
| `ulimit -v` | Virtual memory limit | `ulimit -v unlimited` |

### Network Analysis

| Command | Purpose | Example |
|---------|---------|---------|
| `ss` | Socket statistics | `ss -tunapl` |
| `netstat` | Network statistics | `netstat -tulpn` |
| `iptraf` | Real-time network statistics | `iptraf-ng -i all` |
| `tcpdump` | Packet analyzer | `tcpdump -i eth0` |

### Storage Analysis

| Command | Purpose | Example |
|---------|---------|---------|
| `df` | Disk space usage | `df -h` |
| `du` | Directory space usage | `du -sh *` |
| `iotop` | I/O monitoring | `iotop -o` |
| `lsof` | List open files | `lsof -p PID` |

### Process Management

| Command | Purpose | Example |
|---------|---------|---------|
| `ps` | Process status | `ps aux` |
| `pstree` | Process tree | `pstree -p` |
| `strace` | System call tracer | `strace -p PID` |
| `ltrace` | Library call tracer | `ltrace -p PID` |

### Memory Analysis

| Command | Purpose | Example |
|---------|---------|---------|
| `free` | Memory usage | `free -m` |
| `pmap` | Process memory map | `pmap -x PID` |
| `smem` | Memory reporter | `smem -t` |
| `valgrind` | Memory debugger | `valgrind --leak-check=full` |

### Performance Profiling

| Command | Purpose | Example |
|---------|---------|---------|
| `perf` | Performance analysis | `perf record -a` |
| `oprofile` | System profiler | `operf ./myapp` |
| `gprof` | GNU profiler | `gprof ./myapp` |
| `ftrace` | Function tracer | `trace-cmd record -p function` |

## Best Practices

1. **Monitoring Hierarchy**
   - Start with high-level tools (top, vmstat)
   - Drill down with specific tools (iostat, netstat)
   - Use specialized tools for detailed analysis

2. **Resource Management**
   - Set appropriate limits with ulimit
   - Monitor resource usage regularly
   - Implement proper capacity planning

3. **Performance Tuning**
   - Make one change at a time
   - Document all changes
   - Measure impact before and after

4. **Network Optimization**
   - Monitor bandwidth usage
   - Configure appropriate buffer sizes
   - Use traffic shaping when needed

5. **Storage Performance**
   - Monitor I/O patterns
   - Set appropriate scheduler
   - Optimize filesystem parameters

6. **Process Management**
   - Set appropriate priorities
   - Monitor resource consumption
   - Use cgroups for resource control

## Troubleshooting Guide

### Common Issues and Solutions

1. **High CPU Usage**
```bash
# Identify CPU-intensive processes
top -b -n 1 | head -n 20

# Check process priorities
ps -el | sort -nr -k 4

# Set CPU affinity
taskset -pc 0-3 PID
```

2. **Memory Problems**
```bash
# Check memory usage
free -h
vmstat 1

# Find memory leaks
valgrind --leak-check=full ./application

# Clear page cache
echo 3 > /proc/sys/vm/drop_caches
```

3. **I/O Bottlenecks**
```bash
# Monitor I/O usage
iostat -xz 1

# Check I/O scheduling
cat /sys/block/sda/queue/scheduler

# Set I/O priority
ionice -c 2 -n 0 -p PID
```

4. **Network Issues**
```bash
# Monitor network traffic
iftop -i eth0

# Check network settings
ethtool eth0

# Monitor connections
netstat -tunapl
```
