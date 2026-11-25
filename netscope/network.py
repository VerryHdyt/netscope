
import socket
import psutil
import subprocess
import platform
import ipaddress


def get_local_ip():
    """Detect the primary local IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_network_interfaces():
    """Get available network interfaces."""
    interfaces = []

    stats = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()

    for interface_name, interface_addresses in addresses.items():
        interface_info = {
            "name": interface_name,
            "status": stats[interface_name].isup if interface_name in stats else False,
            "addresses": [],
        }

        for address in interface_addresses:
            if address.family == socket.AF_INET:
                interface_info["addresses"].append({
                    "ip": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast,
                })

        interfaces.append(interface_info)

    return interfaces


def get_default_gateway():
    """Get default gateway based on operating system."""
    system = platform.system()

    try:
        if system == "Linux":
            result = subprocess.check_output(
                ["ip", "route", "show", "default"],
                text=True
            )
            for line in result.splitlines():
                parts = line.split()
                if "via" in parts:
                    return parts[parts.index("via") + 1]

        elif system == "Windows":
            result = subprocess.check_output(
                ["route", "print", "0.0.0.0"],
                text=True
            )
            for line in result.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "0.0.0.0":
                    return parts[2]

        elif system == "Darwin":
            result = subprocess.check_output(
                ["route", "-n", "get", "default"],
                text=True
            )
            for line in result.splitlines():
                if "gateway:" in line:
                    return line.split("gateway:")[1].strip()

    except Exception:
        pass

    return "Unknown"


def get_network_info():
    """Collect basic network information."""
    local_ip = get_local_ip()

    interfaces = get_network_interfaces()
    gateway = get_default_gateway()

    subnet = "Unknown"

    for interface in interfaces:
        for address in interface["addresses"]:
            if address["ip"] == local_ip and address["netmask"]:
                try:
                    network = ipaddress.ip_network(
                        f'{address["ip"]}/{address["netmask"]}',
                        strict=False
                    )
                    subnet = str(network)
                except ValueError:
                    pass

    return {
        "hostname": socket.gethostname(),
        "local_ip": local_ip,
        "subnet": subnet,
        "gateway": gateway,
        "interfaces": interfaces,
    }
