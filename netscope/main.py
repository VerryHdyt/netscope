
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from netscope.report import export_json
from netscope.network import get_network_info
from netscope.discovery import discover_hosts

console = Console()


def display_banner():
    banner = r"""
 _   _      _   _____
| \ | | ___| |_| ____|__  ___ __
|  \| |/ _ \ __|  _| \ \/ / '_ \
| |\  |  __/ |_| |___ >  <| |_) |
|_| \_|\___|\__|_____/_/\_\ .__/
                          |_|
    Local Network Inspector
    """

    console.print(
        Panel(
            Text(banner, style="bold cyan", justify="center"),
            border_style="cyan",
            padding=(1, 2),
        )
    )


def display_network_info(info):
    table = Table(
        title="Network Information",
        border_style="cyan",
    )

    table.add_column("Property", style="bold white")
    table.add_column("Value", style="green")

    table.add_row("Hostname", info["hostname"])
    table.add_row("Local IP", info["local_ip"])
    table.add_row("Subnet", info["subnet"])
    table.add_row("Default Gateway", info["gateway"])

    console.print(table)


def display_interfaces(interfaces):
    table = Table(
        title="Network Interfaces",
        border_style="blue",
    )

    table.add_column("Interface", style="cyan")
    table.add_column("Status")
    table.add_column("IPv4 Address", style="green")
    table.add_column("Netmask")

    for interface in interfaces:
        status = (
            "[green]UP[/green]"
            if interface["status"]
            else "[red]DOWN[/red]"
        )

        ipv4 = "-"
        netmask = "-"

        for address in interface["addresses"]:
            ipv4 = address["ip"]
            netmask = address["netmask"] or "-"

        table.add_row(
            interface["name"],
            status,
            ipv4,
            netmask,
        )

    console.print(table)


def display_discovered_hosts(hosts):
    table = Table(
        title="Network Discovery Results",
        border_style="green",
    )

    table.add_column("#", justify="right", style="dim")
    table.add_column("IP Address", style="cyan")
    table.add_column("Hostname", style="yellow")
    table.add_column("Status", style="green")

    for index, host in enumerate(hosts, start=1):
        table.add_row(
            str(index),
            host["ip"],
            host["hostname"],
            "[green]ONLINE[/green]",
        )

    console.print(table)

    console.print(
        f"\n[bold green]Discovered {len(hosts)} responsive host(s).[/bold green]"
    )


def main():
    display_banner()

    with console.status("[bold green]Analyzing network..."):
        info = get_network_info()

    display_network_info(info)
    display_interfaces(info["interfaces"])
    console.print()

    if info["subnet"] == "Unknown":
        console.print(
            "[yellow]No local IPv4 subnet found; skipping host discovery.[/yellow]"
        )
        hosts = []
    else:
        with console.status("[bold yellow]Discovering authorized local hosts..."):
            hosts = discover_hosts(info["subnet"])

    display_discovered_hosts(hosts)
    report_path = export_json(info, hosts)
    console.print(f"[bold green]Report saved to {report_path}[/bold green]")



if __name__ == "__main__":
    main()
