# Linux Static Performance Tools Cheatsheet

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Performance Analysis Tools by Layer](#performance-analysis-tools-by-layer)
3. [Hardware Layer Tools](#hardware-layer-tools)
4. [Operating System Layer Tools](#operating-system-layer-tools)
5. [Application Layer Tools](#application-layer-tools)
6. [Detailed Tool Reference](#detailed-tool-reference)

## System Architecture Overview

The Linux system architecture consists of multiple layers, each with specific performance monitoring and analysis tools. Here's a detailed breakdown of each layer and its components:

### Hardware Layer
- CPUs
- DRAM
- I/O Controllers
- Network Controllers
- Storage Devices

### Operating System Layer Components
1. Device Drivers
2. Block Device
3. Network Device
4. Virtual Memory
5. File Systems
6. TCP/UDP
7. IP Stack
8. System Call Interface
9. Scheduler
10. Clock Source

### Application Layer
- Applications
- System Libraries
- VFS (Virtual File System)
- Sockets

## Performance Analysis Tools by Layer

### Hardware Level Tools

#### CPU Analysis Tools
```bash
# CPU information and statistics
/proc/cpuinfo    # Detailed CPU information
cpuid            # CPU identification and features
lscpu            # CPU architecture information
cpu-x            # CPU identification tool

# CPU Performance Monitoring
numactl          # NUMA topology and statistics
lstopo           # Hardware topology viewer
dmidecode        # DMI table decoder
```

#### Memory Analysis
```bash
# Memory statistics and information
free -m          # Memory usage overview
vmstat           # Virtual memory statistics
dmidecode        # Memory hardware information

# Memory Performance Tools
lstopo           # Memory topology visualization
numactl          # NUMA memory statistics
```

### Operating System Level Tools

#### File System Tools
```bash
# Disk and Filesystem Analysis
df -h            # Filesystem usage
lsblk            # Block device information
blockdev         # Block device operations
smartctl         # SMART disk monitoring
fdisk -l         # Disk partition information
lsusb            # USB device information

# Advanced Storage Analysis
mdadm            # RAID management and monitoring
dmesg            # Storage device messages
```

#### Network Analysis Tools
```bash
# Basic Network Tools
ip route         # IP routing table
tc              # Traffic control
ethtool         # Network interface settings
iwconfig        # Wireless interface configuration
lldptool        # Link Layer Discovery Protocol tool

# Network Statistics
netstat         # Network statistics
ss              # Socket statistics
ip              # IP configuration and statistics
```

#### System Call Interface Tools
```bash
# System Call Monitoring
strace          # System call tracer
ltrace          # Library call tracer
syscall         # System call information
sysctl          # Kernel parameter configuration
```

#### Scheduler Analysis
```bash
# Scheduler Tools
schedtool       # Process scheduler configuration
chrt            # Real-time scheduler priorities
taskset         # CPU affinity configuration
```

### Application Level Tools

#### Process Analysis
```bash
# Process Monitoring
top             # Process activity monitoring
htop            # Interactive process viewer
ps              # Process status
pstree          # Process hierarchy view
```

#### System Library Analysis
```bash
# Library Tools
ldd             # Shared library dependencies
ldconfig        # Library path configuration
ld              # Link editor for object files
```

## Detailed Tool Reference

### System Information Tools

#### sysctl
```bash
# View all system parameters
sysctl -a

# View specific parameter
sysctl kernel.hostname

# Modify parameter
sysctl -w kernel.hostname=newname

# Load settings from file
sysctl -p /etc/sysctl.conf
```

#### dmesg
```bash
# View kernel messages
dmesg

# Clear kernel ring buffer
dmesg -c

# Show human-readable timestamps
dmesg -T

# Follow new messages
dmesg -w
```

### Storage Performance Tools

#### smartctl
```bash
# Check disk health
smartctl -a /dev/sda

# Run short self-test
smartctl -t short /dev/sda

# Show test results
smartctl -l selftest /dev/sda

# Enable SMART
smartctl -s on /dev/sda
```

#### iostat
```bash
# Basic I/O statistics
iostat

# Extended statistics
iostat -x

# Device utilization
iostat -d

# Updates every 2 seconds
iostat 2
```

### Network Performance Tools

#### ethtool
```bash
# Show interface settings
ethtool eth0

# Show interface statistics
ethtool -S eth0

# Set interface speed
ethtool -s eth0 speed 1000

# Check link status
ethtool -i eth0
```

#### tc (Traffic Control)
```bash
# Show queueing discipline
tc qdisc show

# Add rate limiting
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms

# Show filter rules
tc filter show dev eth0

# Delete all rules
tc qdisc del dev eth0 root
```

### Process Management Tools

#### schedtool
```bash
# Show process scheduler info
schedtool -p 1234

# Set SCHED_FIFO policy
schedtool -F -p 50 1234

# Set CPU affinity
schedtool -a 0-3 1234

# Show all scheduler policies
schedtool -h
```

#### numactl
```bash
# Show NUMA topology
numactl --hardware

# Run command on specific node
numactl --membind=0 command

# Show NUMA statistics
numactl --show

# Set memory policy
numactl --preferred=0 command
```

### Virtual Memory Analysis

#### vmstat
```bash
# Memory statistics
vmstat

# Detailed memory info
vmstat -s

# Active/inactive memory
vmstat -a

# Disk statistics
vmstat -d
```

### Advanced Analysis Tools

#### SystemTap
```bash
# Create simple probe
stap -e 'probe syscall.open { println(execname()) }'

# Monitor file operations
stap -e 'probe vfs.read { printf("%s read %d bytes\n", execname(), count) }'

# Track process creation
stap -e 'probe process.begin { printf("%s started\n", execname()) }'
```

#### perf
```bash
# CPU performance counters
perf stat command

# System-wide sampling
perf record -a sleep 10

# Show recorded data
perf report

# Live performance monitoring
perf top
```

### Hardware Management

#### dmidecode
```bash
# Show all hardware info
dmidecode

# Show memory info
dmidecode -t memory

# Show CPU info
dmidecode -t processor

# Show system info
dmidecode -t system
```

### Volume Management Tools

#### MegaCli
```bash
# Show RAID configuration
MegaCli -CfgDsply -aALL

# Check battery status
MegaCli -AdpBbuCmd -aALL

# Show drive information
MegaCli -PDList -aALL

# Check rebuild status
MegaCli -PDRbld -ShowProg -physdrv[252:2] -aALL
```

### Performance Monitoring Best Practices

1. **Regular Monitoring**
   - Set up baseline measurements
   - Monitor trends over time
   - Create alerts for anomalies

2. **Resource Usage**
   - Track CPU utilization
   - Monitor memory consumption
   - Watch I/O patterns
   - Analyze network traffic

3. **System Health**
   - Check system logs
   - Monitor hardware status
   - Track error rates
   - Verify service status

4. **Performance Optimization**
   - Identify bottlenecks
   - Tune system parameters
   - Optimize application settings
   - Balance resource allocation

### Common Performance Issues and Solutions

1. **CPU Bottlenecks**
   - Use `top` and `htop` to identify high CPU processes
   - Check process priorities with `nice` and `renice`
   - Monitor CPU scheduling with `schedtool`
   - Analyze system load with `uptime`

2. **Memory Problems**
   - Check memory usage with `free` and `vmstat`
   - Monitor swap usage
   - Analyze memory leaks
   - Tune kernel memory parameters

3. **Disk I/O Issues**
   - Monitor disk activity with `iostat`
   - Check disk health with `smartctl`
   - Analyze I/O patterns with `iotop`
   - Optimize filesystem parameters

4. **Network Performance**
   - Monitor bandwidth with `iftop`
   - Analyze connections with `netstat`
   - Check network errors with `ethtool`
   - Tune network parameters with `sysctl`

### Quick Reference Commands

```bash
# System Overview
top                     # Process activity
htop                    # Interactive process viewer
uptime                  # Load average
dmesg                   # Kernel messages

# Memory Analysis
free -m                 # Memory usage
vmstat                  # Virtual memory stats
pmap                    # Process memory map
smem                    # Memory reporting

# Disk Operations
iostat                  # I/O statistics
iotop                   # I/O monitoring
fdisk -l                # Disk partitions
df -h                   # Filesystem usage

# Network Analysis
netstat                 # Network statistics
ss                      # Socket statistics
iftop                   # Network bandwidth
tcpdump                 # Packet analysis

# Process Management
ps aux                  # Process status
pstree                  # Process tree
nice                    # Process priority
renice                  # Change priority

# System Information
uname -a                # System information
lscpu                   # CPU information
lsblk                   # Block devices
lspci                   # PCI devices
```

### Additional Resources

1. **Documentation**
   - Man pages for each tool
   - Linux kernel documentation
   - Distribution-specific guides
   - Tool-specific documentation

2. **Performance Tuning Guides**
   - Red Hat Performance Tuning Guide
   - Ubuntu Server Guide
   - Linux Performance website
   - Kernel documentation

3. **Monitoring Tools**
   - Nagios
   - Zabbix
   - Prometheus
   - Grafana

4. **Training Resources**
   - Linux Foundation courses
   - Distribution certification programs
   - Online tutorials
   - Community forums
