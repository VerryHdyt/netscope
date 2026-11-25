
import json
from datetime import datetime
from pathlib import Path


def export_json(network_info, discovered_hosts):
    """Export network inspection results to JSON."""

    report = {
        "tool": "NetScope",
        "version": "0.1.0",
        "generated_at": datetime.now().astimezone().isoformat(),
        "network": network_info,
        "discovered_hosts": discovered_hosts,
        "summary": {
            "total_hosts": len(discovered_hosts),
            "online_hosts": sum(
                1 for host in discovered_hosts
                if host["status"] == "online"
            ),
        },
    }

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = reports_dir / f"netscope_report_{timestamp}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    return file_path
