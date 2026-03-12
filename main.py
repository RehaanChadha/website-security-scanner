from colorama import Fore, Style, init
from scanner.header_scanner import scan_headers
from scanner.port_scanner import scan_ports
from scanner.ssl_scanner import scan_ssl
from scanner.vulnerability_scanner import scan_vulnerabilities
from utils.report_generator import save_report, save_json_report

init(autoreset=True)


def main():
    print(f"{Fore.CYAN}==============================")
    print("   Website Security Scanner")
    print(f"=============================={Style.RESET_ALL}")

    url = input("Enter website URL (example: https://example.com): ")

    if not url.startswith("http"):
        url = "https://" + url

    domain = url.replace("https://", "").replace("http://", "")

    print(f"\n{Fore.YELLOW}Starting scan for: {url}{Style.RESET_ALL}")

    scan_headers(url)
    scan_ports(domain)
    scan_ssl(domain)
    scan_vulnerabilities(url)

    report_text = f"""Website Security Scan Report
Target: {domain}
URL: {url}

Modules Run:
- Header Scanner
- Port Scanner
- SSL Scanner
- Vulnerability Scanner

Scan Status:
Completed successfully
"""

    report_data = {
        "target": domain,
        "url": url,
        "modules": [
            "header_scanner",
            "port_scanner",
            "ssl_scanner",
            "vulnerability_scanner"
        ],
        "status": "completed"
    }

    report_file = save_report(domain, report_text)
    json_report_file = save_json_report(domain, report_data)

    print(f"\n{Fore.GREEN}Text report saved to: {report_file}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}JSON report saved to: {json_report_file}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()