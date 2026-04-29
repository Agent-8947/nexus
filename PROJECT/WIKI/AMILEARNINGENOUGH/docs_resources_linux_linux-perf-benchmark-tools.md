# Linux Performance Benchmark Tools Guide

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Benchmark Tools by Layer](#benchmark-tools-by-layer)
3. [Hardware Layer Benchmarks](#hardware-layer-benchmarks)
4. [Operating System Layer Benchmarks](#operating-system-layer-benchmarks)
5. [Application Layer Benchmarks](#application-layer-benchmarks)
6. [Network Performance Tools](#network-performance-tools)
7. [Detailed Tool Reference](#detailed-tool-reference)

## System Architecture Overview

The Linux system architecture can be benchmarked at multiple layers using specialized tools. Here's a breakdown of the architecture and associated benchmark tools:

### Hardware Components
- CPUs
- GPUs/TPUs
- DRAM
- HBM (High Bandwidth Memory)
- FPGAs
- I/O Controllers
- Network Controllers
- SMC (System Management Controller)
- Fans

### Operating System Components
1. Device Drivers
2. Block Device
3. Network Device
4. Virtual Memory
5. File Systems
6. TCP/UDP
7. IP Stack
8. System Call Interface
9. Scheduler

### Application Layer
- Applications
- System Libraries
- VFS (Virtual File System)
- Sockets

## Benchmark Tools by Layer

### System Benchmarks

#### sysbench
```bash
# CPU benchmark
sysbench cpu run

# Memory benchmark
sysbench memory run

# File I/O benchmark
sysbench fileio --file-test-mode=seqwr run

# MySQL benchmark
sysbench mysql-oltp-read-write run

# Common options
--threads=4              # Number of threads to use
--time=60               # Test duration in seconds
--events=1000           # Number of events to process
```

#### UnixBench
```bash
# Run complete benchmark suite
./Run

# Run specific tests
./Run dhry2reg
./Run whetstone
./Run execl
./Run file1
./Run shell1

# Multi-CPU tests
./Run -c 4              # Test with 4 copies
```

### Application Level Benchmarks

#### ab (Apache Benchmark)
```bash
# Basic HTTP GET benchmark
ab -n 1000 -c 10 http://localhost/

# POST request benchmark
ab -n 1000 -c 10 -p post.data http://localhost/form

# Common options
-k                      # Use HTTP KeepAlive
-H "Header: value"      # Add custom header
-C "cookie=value"       # Add cookie
-T "content/type"       # Set content-type
```

#### wrk (HTTP Benchmarking Tool)
```bash
# Basic HTTP benchmark
wrk -t12 -c400 -d30s http://localhost

# With custom script
wrk -t2 -c100 -d30s -s script.lua http://localhost

# Common options
-t12                    # 12 threads
-c400                   # 400 connections
-d30s                   # 30 second duration
--timeout 30s           # 30 second timeout
```

### Hardware Benchmarks

#### MLPerf (Machine Learning Performance)
```bash
# Run training benchmark
mlperf-train --config=resnet50 --framework=tensorflow

# Run inference benchmark
mlperf-inference --scenario=Server --model=resnet50

# Common options
--backend=gpu           # Use GPU backend
--precision=fp16        # Use FP16 precision
--dataset=imagenet      # Specify dataset
```

#### perf bench
```bash
# Scheduler benchmarks
perf bench sched pipe
perf bench sched messaging

# Memory benchmarks
perf bench mem memcpy
perf bench mem memset

# Futex benchmarks
perf bench futex wake
perf bench futex wake-parallel
```

### Storage Benchmarks

#### fio (Flexible I/O Tester)
```bash
# Sequential read test
fio --name=seq-read --rw=read --size=4G

# Random write test
fio --name=rand-write --rw=randwrite --bs=4k --size=1G

# Mixed workload
fio --name=mixed --rw=randrw --bs=4k --size=1G

# Common options
--iodepth=16           # I/O queue depth
--direct=1             # Use O_DIRECT
--numjobs=4            # Number of parallel jobs
--runtime=60           # Test duration in seconds
```

#### dd (Disk Performance)
```bash
# Write speed test
dd if=/dev/zero of=test bs=1G count=1 oflag=direct

# Read speed test
dd if=test of=/dev/null bs=1G count=1 iflag=direct

# Common options
bs=1M                  # Block size
count=1000             # Number of blocks
conv=fdatasync         # Sync data before finishing
```

### Network Benchmarks

#### iperf/iperf3
```bash
# Server mode
iperf3 -s

# Client mode TCP test
iperf3 -c server_ip

# UDP bandwidth test
iperf3 -c server_ip -u -b 100M

# Common options
-P 4                   # Number of parallel streams
-i 1                   # Report interval
-t 30                  # Test duration
-w 256K                # Window size
```

#### ttcp (Test TCP)
```bash
# Receiver mode
ttcp -r -s

# Transmitter mode
ttcp -t -s server_ip

# Common options
-l 8192                # Buffer size
-n 2048                # Number of buffers
-p 5001                # Port number
```

### System Call Benchmarks

#### lmbench
```bash
# Run complete benchmark suite
lmbench-run

# Memory latency benchmark
lat_mem_rd 1024 512

# Context switch benchmark
lat_ctx -s 64K 2 4 8 16

# Common options
-P 1                   # Number of processes
-W 3                   # Warmup time
-N 5                   # Number of runs
```

### System Tools

#### jmeter (Application Performance Testing)
```bash
# Run test plan
jmeter -n -t test.jmx -l results.jtl

# Generate HTML report
jmeter -g results.jtl -o report_directory

# Common options
-Jthreads=10           # Number of threads
-Jduration=300         # Test duration
-Jrampup=60            # Ramp-up period
```

### Network Diagnostic Tools

#### hping3
```bash
# TCP SYN flood test
hping3 -S -p 80 --flood target_ip

# ICMP ping test
hping3 -1 target_ip

# Common options
--fast                 # Send packets fast
--rand-source         # Random source address
-i u100               # Wait 100 microseconds between packets
```

#### pchar (Network Performance)
```bash
# Measure path characteristics
pchar network_path

# Common options
-i interface           # Specify interface
-q                     # Quiet mode
-v                     # Verbose output
```

### Hardware Parameter Tools

#### hdparm (Hard Drive Parameters)
```bash
# Disk read timing
hdparm -t /dev/sda

# Cache read timing
hdparm -T /dev/sda

# Common options
-i                     # Show device information
-I                     # Detailed device information
--direct               # Use O_DIRECT
```

## Best Practices for Benchmarking

1. **Preparation**
   - Clean system state
   - Consistent environment
   - Minimal background processes
   - Representative workloads

2. **Execution**
   - Multiple iterations
   - Varying parameters
   - Record all conditions
   - Monitor system state

3. **Analysis**
   - Statistical analysis
   - Outlier detection
   - Performance regression
   - Bottleneck identification

4. **Documentation**
   - Hardware configuration
   - Software versions
   - Test parameters
   - Environmental factors

### Common Benchmarking Scenarios

1. **Web Server Performance**
```bash
# Using ab
ab -n 10000 -c 100 http://localhost/
# Using wrk
wrk -t4 -c100 -d30s http://localhost/
```

2. **Database Performance**
```bash
# Using sysbench
sysbench oltp_read_write --table-size=1000000 prepare
sysbench oltp_read_write --table-size=1000000 run
```

3. **Storage Performance**
```bash
# Using fio
fio --name=randwrite --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --size=4g
```

4. **Network Performance**
```bash
# Using iperf3
iperf3 -c server_ip -t 60 -P 4
```

### Performance Metrics to Monitor

1. **CPU Metrics**
   - Utilization
   - Load average
   - Context switches
   - Cache hits/misses

2. **Memory Metrics**
   - Usage
   - Page faults
   - Swap usage
   - Cache efficiency

3. **Disk Metrics**
   - IOPS
   - Throughput
   - Latency
   - Queue depth

4. **Network Metrics**
   - Bandwidth
   - Latency
   - Packet loss
   - Connection states

### Additional Resources

1. **Documentation**
   - Man pages for tools
   - Vendor documentation
   - Performance tuning guides
   - Benchmark specifications

2. **Monitoring Tools**
   - Grafana
   - Prometheus
   - Telegraf
   - Ganglia

3. **Analysis Tools**
   - R Statistical Software
   - Python with NumPy/Pandas
   - Jupyter Notebooks
   - Excel/LibreOffice Calc

4. **Community Resources**
   - Linux Performance website
   - Performance mailing lists
   - Tool-specific forums
   - Academic papers
