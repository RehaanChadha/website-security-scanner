import argparse
from colorama import Fore, Style, init
from urllib.parse import urlparse
from scanner.header_scanner import scan_headers
from scanner.port_scanner import scan_ports
from scanner.ssl_scanner import scan_ssl
from scanner.vulnerability_scanner import scan_vulnerabilities
from utils.report_generator import save_report, save_json_report

init(autoreset=True)


def normalize_target(raw_input):
    url = raw_input.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        raise ValueError("Please enter a valid website URL or hostname.")

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return {
        "url": url,
        "base_url": base_url,
        "hostname": hostname,
        "report_name": hostname.replace(":", "_")
    }


def scan_has_error(scan_result):
    return "error" in scan_result


def build_parser():
    parser = argparse.ArgumentParser(
        description="Website Security Scanner"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target website or domain (example: github.com)"
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    print(f"{Fore.CYAN}==============================")
    print("   Website Security Scanner")
    print(f"=============================={Style.RESET_ALL}")

    try:
        target = normalize_target(args.target)
    except ValueError as error:
        print(f"{Fore.RED}{error}{Style.RESET_ALL}")
        return

    url = target["url"]
    base_url = target["base_url"]
    domain = target["hostname"]
    report_name = target["report_name"]

    print(f"\n{Fore.YELLOW}Starting scan for: {url}{Style.RESET_ALL}")

    header_results = scan_headers(url)
    port_results = scan_ports(domain)
    ssl_results = scan_ssl(domain)
    vulnerability_results = scan_vulnerabilities(base_url)

    scan_errors = any(
        scan_has_error(result)
        for result in (
            header_results,
            port_results,
            ssl_results,
            vulnerability_results
        )
    )
    scan_status = "completed_with_errors" if scan_errors else "completed"
    status_message = "Completed with errors" if scan_errors else "Completed successfully"

    headers_found_text = ", ".join(header_results.get("headers_found", [])) or "None"
    headers_missing_text = ", ".join(header_results.get("headers_missing", [])) or "None"
    open_ports_text = ", ".join(
        [f"{port['port']} ({port['service']})" for port in port_results.get("open_ports", [])]
    ) or "None"
    interesting_paths_text = ", ".join(
        [item["path"] for item in vulnerability_results.get("interesting_paths", [])]
    ) or "None"

    report_text = f"""Website Security Scan Report
Target: {domain}
URL: {url}

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

    report_data = {
        "target": domain,
        "url": url,
        "status": scan_status,
        "results": {
            "header_scan": header_results,
            "port_scan": port_results,
            "ssl_scan": ssl_results,
            "vulnerability_scan": vulnerability_results
        }
    }

    report_file = save_report(report_name, report_text)
    json_report_file = save_json_report(report_name, report_data)

    print(f"\n{Fore.GREEN}Text report saved to: {report_file}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}JSON report saved to: {json_report_file}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()