
# NetScope

<p align="center">
  <strong>A lightweight local network discovery and monitoring tool built with Python.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

NetScope is a command-line network inspection tool designed to help users understand and explore their local network. It automatically detects network configuration, identifies active hosts, displays network interfaces, and generates JSON reports.

Built with Python and Rich, NetScope provides a clean and readable terminal interface for local network diagnostics.

## Features

- **Network Information** — Detect local IP address, subnet, and default gateway.
- **Interface Monitoring** — Display available network interfaces and their status.
- **Host Discovery** — Identify responsive devices within the local network.
- **Hostname Resolution** — Attempt reverse DNS lookup for discovered hosts.
- **MAC Address Lookup** — Retrieve MAC addresses from the local ARP cache.
- **JSON Reporting** — Export network inspection results to JSON.
- **Terminal Dashboard** — Display network information using a Rich-powered interface.
- **Lightweight** — Simple Python-based tool with minimal dependencies.

## Preview

```text
╭──────────────────────────────────────────────╮
│                 NetScope                    │
│          Local Network Inspector            │
╰──────────────────────────────────────────────╯

Network Information
  Hostname      : localhost
  Local IP      : 192.168.1.15
  Subnet        : 192.168.1.0/24
  Gateway       : 192.168.1.1
  Interface     : en0

Discovered Hosts
  192.168.1.1   Responsive
  192.168.1.12  Responsive
  192.168.1.15  Responsive
  192.168.1.17  Responsive
```

## Requirements

- Python 3.10 or newer
- macOS, Linux, or Windows
- A local network you own or are authorized to inspect

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VerryHdyt/netscope.git
cd netscope
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run NetScope from the project directory:

```bash
python -m netscope.main
```

NetScope automatically detects the local network configuration and performs host discovery on the detected subnet.

## JSON Reports

NetScope generates JSON reports containing network information and discovery results.

Reports are saved in:

```text
reports/
```

Example report structure:

```json
{
  "network": {
    "hostname": "localhost",
    "local_ip": "192.168.1.15",
    "subnet": "192.168.1.0/24",
    "gateway": "192.168.1.1"
  },
  "discovered_hosts": [],
  "summary": {
    "total_hosts": 4
  }
}
```

Generated reports are excluded from version control to protect local network information.

## Project Structure

```text
netscope/
├── netscope/
│   ├── __init__.py
│   ├── main.py
│   ├── network.py
│   ├── discovery.py
│   └── report.py
├── tests/
├── reports/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Technologies

- Python
- psutil
- Rich
- Socket
- Subprocess
- JSON

## Roadmap

- [x] Local network information detection
- [x] Network interface inspection
- [x] Host discovery
- [x] Reverse DNS lookup
- [x] JSON report generation
- [ ] MAC address display improvements
- [ ] Port scanning for authorized local devices
- [ ] Network latency monitoring
- [ ] Historical network monitoring
- [ ] Export reports to CSV

## Disclaimer

NetScope is intended for educational purposes, network diagnostics, and authorized network inspection.

Only use this tool on networks you own or have explicit permission to inspect. The accuracy of host discovery depends on network configuration, device availability, firewall rules, and operating system behavior.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with Python by <a href="https://github.com/VerryHdyt">VerryHdyt</a>
</p>
