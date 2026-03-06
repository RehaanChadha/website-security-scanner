from colorama import Fore, Style, init
from scanner.header_scanner import scan_headers
from scanner.port_scanner import scan_ports
from scanner.ssl_scanner import scan_ssl

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


if __name__ == "__main__":
    main()