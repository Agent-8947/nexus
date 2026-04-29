# Every Linux Networking Tool You Need to Know

This comprehensive cheatsheet covers a wide range of Linux networking tools, providing a one-stop reference for Linux users.

## `ping`
The `ping` command is used to check if a remote computer is reachable on a network. It sends ICMP echo request packets to the target host and waits for a response.

**Usage Examples:**
- `ping <hostname>`: Sends ICMP echo requests to the specified hostname.
- `ping <IP_address>`: Sends ICMP echo requests to the specified IP address.
- `ping -c <count> <target>`: Sends a specified number of ICMP echo requests and then exits.
- `ping -i <interval> <target>`: Sets the interval between sent packets in seconds.
- `ping -s <size> <target>`: Specifies the size of the ICMP echo request packet.

## `curl`
`curl` is a versatile tool for making HTTP requests, providing more control and flexibility than `ping`. It supports a wide range of protocols, including HTTP, FTP, SFTP, and more.

**Usage Examples:**
- `curl <URL>`: Sends a GET request to the specified URL and outputs the response.
- `curl -X POST -d "data=value" <URL>`: Sends a POST request with form data.
- `curl -H "Content-Type: application/json" -d '{"key":"value"}' <URL>`: Sends a POST request with JSON data.
- `curl -o <filename> <URL>`: Saves the response to a file instead of printing it to the console.
- `curl -L <URL>`: Follows redirects automatically.

## `httpie`
`httpie` is a user-friendly command-line tool for making HTTP requests. It has a more intuitive syntax compared to `curl`, making it easier to use for some users.

**Usage Examples:**
- `http <URL>`: Sends a GET request to the specified URL.
- `http POST <URL> key=value`: Sends a POST request with form data.
- `http PUT <URL> key:value`: Sends a PUT request with JSON data.
- `http -h`: Displays the available options and headers.
- `http --json <URL> key=value`: Sends a POST request with JSON data.

## `wget`
`wget` is a command-line tool used for downloading files from the web. It supports recursive downloads, mirroring, and background downloads.

**Usage Examples:**
- `wget <URL>`: Downloads the file at the specified URL.
- `wget -c <URL>`: Resumes a partially downloaded file.
- `wget -r <URL>`: Recursively downloads all linked files from the specified URL.
- `wget -b <URL>`: Runs the download in the background.
- `wget -O <filename> <URL>`: Saves the downloaded file with a specific filename.

## `tc`
`tc` (Traffic Control) is a Linux command-line tool used for fine-grained control over network traffic on a Linux router. It allows you to control your brother's internet bandwidth and other network-related settings.

**Usage Examples:**
- `tc qdisc add dev <interface> root tbf rate <rate> burst <burst> lat <latency>`: Adds a Token Bucket Filter (TBF) to the specified network interface with the given rate, burst, and latency parameters.
- `tc qdisc del dev <interface> root`: Removes the traffic control settings for the specified network interface.
- `tc class add dev <interface> parent <parent_class> classid <class_id> tbf rate <rate> burst <burst> lat <latency>`: Adds a TBF class to the specified network interface.
- `tc filter add dev <interface> protocol ip parent <parent_class> u32 match ip dst <IP_address>/<mask> flowid <class_id>`: Adds a filter to the specified network interface to map traffic to a specific class.

## `dig/nslookup`
`dig` (Domain Information Groper) and `nslookup` are tools used to look up the IP address for a given domain name.

**Usage Examples:**
- `dig <domain>`: Performs a DNS lookup for the specified domain and displays the results.
- `dig @<nameserver> <domain>`: Performs a DNS lookup using the specified nameserver.
- `dig -x <IP_address>`: Performs a reverse DNS lookup to find the domain name associated with the given IP address.
- `nslookup <domain>`: Performs a DNS lookup for the specified domain and displays the results.
- `nslookup -type=<record_type> <domain>`: Performs a DNS lookup for a specific record type (e.g., A, MX, NS).

## `whois`
The `whois` command is used to check if a domain is registered and to retrieve information about the domain's registration.

**Usage Examples:**
- `whois <domain>`: Retrieves the registration information for the specified domain.
- `whois -h <whois_server> <domain>`: Queries a specific WHOIS server for the domain information.
- `whois -a <domain>`: Displays the full WHOIS record for the domain, including contact information.
- `whois -r <domain>`: Checks the availability of the specified domain.

## `ssh`
`ssh` (Secure Shell) is a command-line tool used to establish a secure connection to a remote server or computer.

**Usage Examples:**
- `ssh <username>@<remote_host>`: Connects to the specified remote host with the given username.
- `ssh -p <port> <username>@<remote_host>`: Connects to the remote host using the specified port.
- `ssh -i <private_key_file> <username>@<remote_host>`: Connects to the remote host using the specified private key file for authentication.
- `ssh-keygen -t rsa -b 4096 -C "<comment>"`: Generates a new RSA SSH key pair with the specified comment.
- `ssh-copy-id <username>@<remote_host>`: Copies the local user's public key to the remote host's authorized_keys file.

## `scp`
`scp` (Secure Copy) is a command-line tool used to securely copy files between a local and a remote system over an SSH connection.

**Usage Examples:**
- `scp <local_file> <username>@<remote_host>:<remote_path>`: Copies a local file to a remote system.
- `scp <username>@<remote_host>:<remote_file> <local_path>`: Copies a file from a remote system to the local machine.
- `scp -r <local_directory> <username>@<remote_host>:<remote_path>`: Recursively copies a local directory to a remote system.
- `scp -P <port> <source> <destination>`: Specifies the port to use for the SSH connection.
- `scp -i <private_key_file> <source> <destination>`: Uses the specified private key file for authentication.

## `rsync`
`rsync` is a command-line tool used to efficiently synchronize files and directories between a local and a remote system over an SSH connection. It only transfers the changed parts of files, which can save a significant amount of time and bandwidth.

**Usage Examples:**
- `rsync -avz <source_directory> <username>@<remote_host>:<destination_directory>`: Synchronizes a local directory to a remote system, preserving permissions and timestamps, and using compression.
- `rsync -avz <username>@<remote_host>:<source_directory> <local_directory>`: Synchronizes a remote directory to the local system.
- `rsync -avz --delete <source_directory> <username>@<remote_host>:<destination_directory>`: Synchronizes a local directory to a remote system, deleting files on the remote that are not present in the local directory.
- `rsync -avz --exclude <pattern> <source_directory> <username>@<remote_host>:<destination_directory>`: Synchronizes a local directory to a remote system, excluding files or directories that match the specified pattern.
- `rsync -avz --partial --progress <source> <destination>`: Resumes a partially transferred file and shows the progress during the transfer.

## `grep`
`grep` is a command-line tool used to search for and match patterns in text data, including network output.

**Usage Examples:**
- `grep <pattern> <file>`: Searches for the specified pattern in the given file and displays the matching lines.
- `grep -i <pattern> <file>`: Performs a case-insensitive search for the pattern.
- `grep -r <pattern> <directory>`: Recursively searches for the pattern in all files within the specified directory.
- `grep -v <pattern> <file>`: Displays the lines that do not match the specified pattern.
- `grep -n <pattern> <file>`: Displays the line numbers of the matching lines.

## `tcpdump`
`tcpdump` is a powerful command-line tool used for capturing and analyzing network packets on a specific network interface.

**Usage Examples:**
- `tcpdump -i <interface>`: Captures packets on the specified network interface.
- `tcpdump -n -i <interface> port <port>`: Captures packets on the specified port, without resolving hostnames.
- `tcpdump -r <pcap_file>`: Analyzes a previously captured packet capture (PCAP) file.
- `tcpdump -w <pcap_file> -i <interface>`: Captures packets and saves them to a PCAP file.
- `tcpdump -D`: Lists the available network interfaces that can be used for capturing packets.

## `wireshark`
`wireshark` is a graphical network protocol analyzer that provides a powerful GUI for capturing, analyzing, and visualizing network packets.

**Usage Examples:**
- `wireshark`: Starts the Wireshark application, allowing you to select a network interface and begin capturing packets.
- `wireshark -i <interface>`: Starts Wireshark and immediately begins capturing packets on the specified network interface.
- `wireshark -r <pcap_file>`: Opens a previously captured PCAP file in Wireshark for analysis.
- `wireshark -k`: Starts Wireshark and immediately begins capturing packets (the `-k` option starts the capture automatically).
- `wireshark -f "<capture_filter>"`: Starts Wireshark and applies the specified capture filter to the packet capture.

## `arp`
`arp` (Address Resolution Protocol) is a command-line tool used to display and manage the system's ARP table, which maps IP addresses to MAC addresses.

**Usage Examples:**
- `arp -a`: Displays the current ARP table, showing the IP-to-MAC address mappings.
- `arp -d <IP_address>`: Deletes the specified IP address from the ARP table.
- `arp -s <IP_address> <MAC_address>`: Statically adds an IP-to-MAC address mapping to the ARP table.
- `arp -v`: Displays the ARP table with verbose output, including the network interface and timestamp information.
- `arp -n`: Displays the ARP table without resolving hostnames.

## `ip`
The `ip` command is a more comprehensive tool for managing network interfaces and routing compared to the older `ifconfig` command.

**Usage Examples:**
- `ip addr show`: Displays information about all network interfaces, including their IP addresses and MAC addresses.
- `ip link set <interface> up/down`: Brings the specified network interface up or down.
- `ip route show`: Displays the current routing table.
- `ip route add default via <gateway>`: Adds a default gateway to the routing table.
- `ip neigh show`: Displays the neighbor (ARP) table, which maps IP addresses to MAC addresses.

## `route`
The `route` command is used to view and manipulate the kernel's IP routing table.

**Usage Examples:**
- `route -n`: Displays the routing table without resolving hostnames.
- `route add -net <network>/<mask> gw <gateway>`: Adds a new route to the routing table.
- `route del -net <network>/<mask>`: Deletes a route from the routing table.
- `route -C`: Displays the kernel's routing cache, which is used for faster lookups.
- `route -v`: Displays the routing table with verbose output.

## `nmap`
`nmap` (Network Mapper) is a powerful tool for network discovery and security auditing. It can be used to scan networks and identify active hosts and open ports.

**Usage Examples:**
- `nmap <target_host>`: Performs a basic TCP connect scan on the specified target host.
- `nmap -sV <target_host>`: Performs a version scan to determine the running services and their versions on the target host.
- `nmap -sU -p <port> <target_host>`: Performs a UDP scan on the specified port of the target host.
- `nmap -p- <target_host>`: Scans all 65,535 TCP ports on the target host.
- `nmap -sS -p22,80,443 <target_host>`: Performs a SYN scan on the specified ports of the target host.

## `zenmap`
`zenmap` is the graphical user interface (GUI) for the `nmap` tool, providing a more user-friendly experience for network scanning and exploration.

**Usage Examples:**
- `zenmap`: Starts the Zenmap GUI application.
- `zenmap <target_host>`: Starts Zenmap and immediately scans the specified target host.
- `zenmap -p22,80,443 <target_host>`: Starts Zenmap and scans the specified ports on the target host.
- `zenmap -sV <target_host>`: Starts Zenmap and performs a version scan on the target host.
- `zenmap -oX <output_file> <target_host>`: Starts Zenmap, scans the target host, and saves the results to an XML file.

## `p0f`
`p0f` is a passive TCP/IP fingerprinting tool that can be used to identify the operating system of network hosts by analyzing their TCP/IP stack behavior.

**Usage Examples:**
- `p0f -i <interface>`: Runs `p0f` in passive mode, listening on the specified network interface for traffic.
- `p0f -r <pcap_file>`: Analyzes a previously captured packet capture (PCAP) file.
- `p0f -p <pid>`: Attaches `p0f` to the specified process and analyzes its network traffic.
- `p0f -s <socket>`: Connects to the specified Unix domain socket and analyzes the traffic.
- `p0f -U`: Runs `p0f` in interactive mode, displaying the identified operating systems in real-time.

## `openvpn`
`openvpn` is a command-line tool used to establish a secure Virtual Private Network (VPN) connection.

**Usage Examples:**
- `openvpn --config <config_file>`: Starts OpenVPN using the specified configuration file.
- `openvpn --client --remote <server_address> --auth-user-pass <credentials_file>`: Starts OpenVPN in client mode, connecting to the specified server with user credentials.
- `openvpn --server --dev tun --ifconfig <local_ip> <remote_ip>`: Starts OpenVPN in server mode, creating a TUN interface with the specified IP addresses.
- `openvpn --status <status_file>`: Outputs the current status of the OpenVPN connection to the specified file.
- `openvpn --log <log_file>`: Writes the OpenVPN logs to the specified file.

## `wireguard`
`wireguard` is a command-line tool used to manage the WireGuard VPN protocol, which is a newer, faster, and more secure alternative to OpenVPN.

**Usage Examples:**
- `wg-quick up <interface>`: Brings up a WireGuard interface and establishes the VPN connection.
- `wg-quick down <interface>`: Tears down the WireGuard VPN connection and brings the interface down.
- `wg show <interface>`: Displays the current status and configuration of the WireGuard interface.
- `wg set <interface> peer <public_key> endpoint <server_address>:<port>`: Adds a new peer (server) to the WireGuard interface configuration.
- `wg-quick save <interface>`: Saves the current WireGuard interface configuration to a file.

## netcat (nc)

`netcat` (or `nc`) is a versatile network utility that can be used for a variety of tasks, including:

**Usage Examples:**

* `nc -l -p <port>`: Listens on the specified port for incoming connections.
* `nc <host> <port>`: Connects to the specified host and port.
* `nc -u -l -p <port>`: Listens on the specified port for incoming UDP connections.
* `nc -u <host> <port>`: Connects to the specified host and port using UDP.
* `nc -e <program> <host> <port>`: Executes the specified program upon connection.
* `nc -c <shell> <host> <port>`: Executes the specified shell upon connection.
* `nc -z <host> <start_port>-<end_port>`: Performs a TCP port scan on the specified port range.
* `nc -vv <host> <port>`: Connects to the specified host and port in verbose mode.
* `nc -w <timeout> <host> <port>`: Sets a timeout for the connection attempt.
* `nc -4`: Forces netcat to use IPv4.
* `nc -6`: Forces netcat to use IPv6.

## socat

`socat` is a command-line tool that can be used to proxy a TCP socket to a UNIX domain socket, allowing for more complex network setups.

**Usage Examples:**

* `socat TCP4-LISTEN:<port>,reuseaddr,fork UNIX-CONNECT:/path/to/socket`: Listens on the specified port and forwards the connection to a UNIX domain socket.
* `socat UNIX-LISTEN:/path/to/socket,fork TCP4:<remote_host>:<remote_port>`: Listens on a UNIX domain socket and forwards the connection to a remote TCP host and port.
* `socat - TCP4:<remote_host>:<remote_port>`: Creates a simple TCP client, connecting to the specified remote host and port.
* `socat - SYSTEM:'<command>'`: Executes a system command and uses the standard input/output as a socket.
* `socat -d -d FILE:/path/to/file TCP4-LISTEN:<port>`: Listens on a port and logs all traffic to a file.


## tftp/tftp3

`tftp` (Trivial File Transfer Protocol) is a simple file transfer protocol that can be used to transfer files, often for booting diskless systems or embedded devices.

**Usage Examples:**

* `tftp <host>`: Enters the interactive TFTP prompt, allowing you to transfer files.
* `tftp <host> get <remote_file> <local_file>`: Downloads a file from the remote host to the local file.
* `tftp <host> put <local_file> <remote_file>`: Uploads a file from the local system to the remote host.
* `tftp -l <local_file> -r <remote_file> <host>`: Downloads a file from the remote host to the specified local file.
* `tftp -c get <remote_file> <local_file> <host>`: Performs a one-time file download without entering the interactive prompt.


## iptables

`iptables` is the command-line tool used to configure the Linux kernel's Netfilter firewall and Network Address Translation (NAT) rules.

**Usage Examples:**

* `iptables -L`: Lists the current firewall rules.
* `iptables -A <chain> -j <target>`: Appends a new rule to the specified chain.
* `iptables -I <chain> <rule_number> -j <target>`: Inserts a new rule at the specified position in the chain.
* `iptables -D <chain> <rule_number>`: Deletes the specified rule from the chain.
* `iptables -t <table> <commands>`: Applies the specified commands to the given table (e.g., nat, mangle, raw).


## nftables

`nftables` is a newer and more flexible firewall and packet filtering framework that replaces the older `iptables` tool.

**Usage Examples:**

* `nft add table ip filter`: Creates a new IP filter table.
* `nft add chain ip filter forward { type filter hook forward priority 0; }`: Creates a new forward chain in the IP filter table.
* `nft add rule ip filter forward ip protocol tcp drop`: Adds a rule to the forward chain to drop all TCP traffic.
* `nft list ruleset`: Displays the current nftables ruleset.
* `nft flush chain ip filter forward`: Flushes all rules from the specified chain.


## hping3

`hping3` is a command-line tool used to construct custom TCP/IP packets, making it useful for network testing and security assessments.

**Usage Examples:**

* `hping3 --syn --spoof <src_ip> <dst_ip>`: Sends a SYN packet with a spoofed source IP address to the specified destination.
* `hping3 --udp --rand-source <dst_ip> --port <dst_port>`: Sends random source UDP packets to the specified destination and port.
* `hping3 --icmp --flood <dst_ip>`: Sends a flood of ICMP echo request packets to the specified destination.
* `hping3 --scan <start_port>-<end_port> <dst_ip>`: Performs a port scan on the specified IP address and port range.
* `hping3 --listen`: Listens for incoming packets and displays their contents.


## traceroute/mtr

`traceroute` and `mtr` (My TraceRoute) are tools used to trace the network path to a remote host, displaying the latency and hop information along the way.

**Usage Examples:**

* `traceroute <host>`: Traces the network path to the specified host, displaying each hop and the round-trip time.
* `traceroute -n <host>`: Disables DNS lookup, showing the IP addresses instead of hostnames.
* `traceroute -p <port> <host>`: Specifies the destination port to use for the trace.
* `mtr <host>`: Starts the interactive mtr tool, which provides a continuously updated traceroute-like display.
* `mtr --report <host>`: Runs mtr in report mode, generating a single report and then exiting.


## tcptrace

`tcptrace` is a command-line tool used to analyze TCP dump files, providing insights into TCP connections and performance.

**Usage Examples:**

* `tcptrace <pcap_file>`: Analyzes the specified packet capture (PCAP) file and displays detailed information about the TCP connections.
* `tcptrace --all-connections <pcap_file>`: Displays information about all TCP connections in the PCAP file.
* `tcptrace --csv <pcap_file>`: Exports the TCP connection data to a CSV file.
* `tcptrace --plot-tcptrace <pcap_file>`: Generates a TCP connection flow graph from the PCAP file.
* `tcptrace --hints <pcap_file>`: Provides hints and suggestions based on the analysis of the TCP connections.


## ethtool

`ethtool` is a command-line tool used to manage and configure Ethernet-based network device settings, such as link speed, duplex mode, and more.

**Usage Examples:**

* `ethtool <interface>`: Displays the current configuration of the specified network interface.
* `ethtool -s <interface> speed <speed> duplex <mode>`: Sets the speed and duplex mode of the network interface.
* `ethtool -g <interface>`: Displays the ring buffer parameters for the network interface.
* `ethtool -k <interface>`: Displays the offload feature settings for the network interface.
* `ethtool -i <interface>`: Displays the driver information for the network interface.


## iwconfig/iw

`iwconfig` and `iw` are tools used to configure wireless network settings, such as SSID, encryption, and other parameters.

**Usage Examples:**

* `iwconfig <interface> mode managed essid <SSID>`: Sets the wireless interface to managed mode and configures the SSID.
* `iwconfig <interface> freq <frequency>`: Sets the frequency or channel of the wireless interface.
* `iwconfig <interface> key <key>`: Sets the encryption key for the wireless interface.
* `iw dev <interface> set type managed`: Sets the wireless interface to managed mode.
* `iw dev <interface> scan`: Scans for available wireless networks.


## sysctl

`sysctl` is a command-line tool used to configure Linux kernel parameters at runtime, allowing you to tune network-related settings.

**Usage Examples:**

* `sysctl -a`: Lists all available kernel parameters.
* `sysctl net.ipv4.ip_forward`: Displays the current value of the `net.ipv4.ip_forward` kernel parameter.
* `sysctl -w net.ipv4.ip_forward=1`: Sets the `net.ipv4.ip_forward` kernel parameter to 1, enabling IP forwarding.
* `sysctl -p`: Loads the kernel parameters from the `/etc/sysctl.conf` file.
* `sysctl -w net.core.somaxconn=1024`: Sets the maximum number of queued connection requests.


## openssl

`openssl` is a command-line tool used to generate and manage SSL/TLS certificates, which are used for secure network connections.

**Usage Examples:**

* `openssl req -new -x509 -keyout <key_file> -out <cert_file>`: Generates a new self-signed X.509 certificate and private key.
* `openssl x509 -in <cert_file> -text -noout`: Displays the contents of an X.509 certificate.
* `openssl rsa -in <key_file> -check`: Verifies the integrity of a private key.
* `openssl s_client -connect <host>:<port>`: Establishes a TLS connection to the specified host and port.
* `openssl dhparam -out <dhparam_file> 2048`: Generates Diffie-Hellman parameters for use in TLS configurations.


## stunnel

`stunnel` is a command-line tool used to create an SSL/TLS proxy, which can be used to secure network connections to an insecure server.

**Usage Examples:**

* `stunnel <config_file>`: Runs stunnel using the specified configuration file.
* `stunnel -p <cert_file> -k <key_file>`: Runs stunnel with the specified certificate and private key files.
* `stunnel -c -d <local_port> -r <remote_host>:<remote_port>`: Runs stunnel in client mode, forwarding local connections to a remote host and port.
* `stunnel -l <local_port> -r <remote_host>:<remote_port>`: Runs stunnel in server mode, accepting local connections and forwarding them to a remote host and port.
* `stunnel -v`: Runs stunnel in verbose mode, providing more detailed logging.


## iptraf/nethogs

`iptraf` and `nethogs` are command-line tools used to provide real-time information about network bandwidth usage and performance.

**Usage Examples:**

* `iptraf -i <interface>`: Runs the interactive iptraf tool, displaying network traffic statistics for the specified interface.
* `iptraf -s <interface>`: Runs iptraf in server mode, writing the traffic statistics to a log file.
* `nethogs <interface>`: Runs the nethogs tool, which displays the network traffic per process.
* `nethogs -t`: Runs nethogs in terse mode, showing only the process names and their network usage.
* `nethogs -u`: Runs nethogs in user mode, showing the network usage per user instead of per process.


## ab/JMeter/wrk

`ab` (Apache Bench), `JMeter`, and `wrk` are popular benchmarking tools used for testing the performance of web servers and APIs.

**Usage Examples:**

* `ab -n <requests> -c <concurrency> <url>`: Runs the Apache Bench tool, performing the specified number of requests with the given concurrency level.
* `jmeter -n -t <jmx_file> -l <results_file>`: Runs JMeter in non-GUI mode, using the specified test plan file and writing the results to a file.
* `wrk -t<threads> -c<connections> -d<duration> <url>`: Runs the wrk tool, simulating the specified number of threads and connections for the given duration.
* `jmeter -h`: Displays the help menu for the JMeter command-line options.
* `wrk --latency <url>`: Runs wrk and displays the latency statistics in addition to the throughput.


## python -m SimpleHTTPServer

The `python -m SimpleHTTPServer` command can be used to quickly serve files from the current directory using a simple HTTP server.

**Usage Examples:**

* `python -m SimpleHTTPServer <port>`: Starts a simple HTTP server on the specified port, serving files from the current directory.
* `python -m http.server <port>`: The Python 3 equivalent of the above command, starting a simple HTTP server on the specified port.
* `python -m SimpleHTTPServer`: Starts a simple HTTP server on the default port 8000, serving files from the current directory.
* `python -m http.server`: The Python 3 equivalent of the above command, starting a simple HTTP server on the default port 8000.
* `python -m SimpleHTTPServer --help`: Displays the available options for the SimpleHTTPServer module.


## ipcalc

`ipcalc` is a command-line tool used to calculate IP addresses and subnet information.

**Usage Examples:**

* `ipcalc <ip_address> <subnet_mask>`: Calculates the network address, broadcast address, and available host range for the specified IP address and subnet mask.
* `ipcalc -c <cidr_notation>`: Calculates the subnet mask and other information based on the CIDR notation.
* `ipcalc -n <network_address> <prefix_length>`: Calculates the network information based on the network address and prefix length.
* `ipcalc -h`: Displays the help menu for the ipcalc tool, including all available options and usage examples.
* `ipcalc -v`: Displays the version information for the ipcalc tool.


## nsenter

`nsenter` is a command-line tool used to enter a container's network namespace, allowing you to troubleshoot and manage the container's network settings.

**Usage Examples:**

* `nsenter -t <container_pid> -n <command>`: Runs the specified command in the context of the container's network namespace.
* `nsenter -t <container_pid> -n ip addr`: Displays the network interfaces and IP addresses within the container's network namespace.
* `nsenter -t <container_pid> -n ip route`: Displays the routing table within the container's network namespace.
* `nsenter -t <container_pid> -n tcpdump -i eth0`: Captures network traffic within the container's network namespace.
* `nsenter -t <container_pid> -n /bin/bash`: Starts an interactive shell within the context of the container's network namespace.