from urllib.parse import urlparse

from scanner.header_scanner import scan_headers
from scanner.port_scanner import scan_ports
from scanner.ssl_scanner import scan_ssl
from scanner.vulnerability_scanner import scan_vulnerabilities


def normalize_target(raw_input):
    if raw_input is None:
        raise ValueError("Enter a website URL or hostname to scan.")

    url = raw_input.strip()
    if not url:
        raise ValueError("Enter a website URL or hostname to scan.")

    if "://" not in url:
        url = "https://" + url

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if parsed_url.scheme not in ("http", "https"):
        raise ValueError("Enter a valid website URL or hostname.")

    if not hostname:
        raise ValueError("Enter a valid website URL or hostname.")

    if any(character.isspace() for character in hostname):
        raise ValueError("Enter a valid website URL or hostname.")

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return {
        "url": url,
        "base_url": base_url,
        "hostname": hostname,
        "report_name": hostname.replace(":", "_"),
    }


def scan_has_error(scan_result):
    return "error" in scan_result


def build_report_text(report_data):
    results = report_data["results"]
    header_results = results["header_scan"]
    port_results = results["port_scan"]
    ssl_results = results["ssl_scan"]
    vulnerability_results = results["vulnerability_scan"]

    headers_found_text = ", ".join(header_results.get("headers_found", [])) or "None"
    headers_missing_text = ", ".join(header_results.get("headers_missing", [])) or "None"
    open_ports_text = ", ".join(
        [
            f"{port['port']} ({port['service']})"
            for port in port_results.get("open_ports", [])
        ]
    ) or "None"
    interesting_paths_text = ", ".join(
        [item["path"] for item in vulnerability_results.get("interesting_paths", [])]
    ) or "None"

    status_message = (
        "Completed with errors"
        if report_data["status"] == "completed_with_errors"
        else "Completed successfully"
    )

    return f"""Website Security Scan Report
Target: {report_data['target']}
URL: {report_data['url']}

Header Scan:
- Status Code: {header_results.get('status_code')}
- Headers Found: {headers_found_text}
- Headers Missing: {headers_missing_text}

Port Scan:
- Open Ports: {open_ports_text}

SSL Scan:
- Issuer: {ssl_results.get('issuer')}
- Expiry Date: {ssl_results.get('expiry_date')}
- Days Remaining: {ssl_results.get('days_remaining')}

Vulnerability Scan:
- HTTPS Used: {vulnerability_results.get('https_used')}
- Server Header: {vulnerability_results.get('server_header')}
- X-Powered-By: {vulnerability_results.get('x_powered_by')}
- Interesting Paths: {interesting_paths_text}

Scan Status:
{status_message}
"""


def run_scan(raw_target, verbose=False):
    target = normalize_target(raw_target)

    header_results = scan_headers(target["url"], verbose=verbose)
    port_results = scan_ports(target["hostname"], verbose=verbose)
    ssl_results = scan_ssl(target["hostname"], verbose=verbose)
    vulnerability_results = scan_vulnerabilities(target["base_url"], verbose=verbose)

    scan_errors = any(
        scan_has_error(result)
        for result in (
            header_results,
            port_results,
            ssl_results,
            vulnerability_results,
        )
    )

    report_data = {
        "target": target["hostname"],
        "url": target["url"],
        "status": "completed_with_errors" if scan_errors else "completed",
        "results": {
            "header_scan": header_results,
            "port_scan": port_results,
            "ssl_scan": ssl_results,
            "vulnerability_scan": vulnerability_results,
        },
    }

    return {
        "target": target,
        "report_data": report_data,
        "report_text": build_report_text(report_data),
    }
