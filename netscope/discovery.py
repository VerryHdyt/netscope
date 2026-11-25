
import subprocess
import platform
import ipaddress
import re
import socket
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    """Check whether a host responds to ping."""

    system = platform.system()

    if system == "Windows":
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    elif system == "Darwin":
        command = ["ping", "-c", "1", "-W", "1000", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )

        return result.returncode == 0

    except (subprocess.TimeoutExpired, OSError):
        return False



def resolve_mac(ip):
    """Retrieve MAC address from the local ARP cache."""

    try:
        result = subprocess.run(
            ["arp", "-n", str(ip)],
            capture_output=True,
            text=True,
            timeout=2,
        )

        match = re.search(
            r"(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})",
            result.stdout,
        )

        if match:
            return match.group(1).upper()

    except (subprocess.TimeoutExpired, OSError):
        pass

    return "Unknown"


def resolve_hostname(ip):
    """Resolve a host's name, falling back to its IP address."""
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except OSError:
        return str(ip)



def scan_host(ip):
    """Scan a host and collect basic information."""

    if ping_host(ip):
        return {
            "ip": str(ip),
            "hostname": resolve_hostname(ip),
            "status": "online",
        }

    return None


def discover_hosts(subnet):
    """Return responsive hosts in a subnet."""
    network = ipaddress.ip_network(subnet, strict=False)

    with ThreadPoolExecutor() as executor:
        results = executor.map(scan_host, network.hosts())
        return [host for host in results if host is not None]

