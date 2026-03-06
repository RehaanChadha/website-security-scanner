import nmap
from colorama import Fore, Style


def scan_ports(target):
    try:
        scanner = nmap.PortScanner()

        print(f"\n{Fore.CYAN}Scanning Open Ports for: {target}{Style.RESET_ALL}\n")

        scanner.scan(hosts=target, arguments="-F")

        if not scanner.all_hosts():
            print(f"{Fore.RED}No host found or target is unreachable.{Style.RESET_ALL}")
            return

        host = scanner.all_hosts()[0]

        for protocol in scanner[host].all_protocols():
            ports = scanner[host][protocol].keys()

            for port in sorted(ports):
                state = scanner[host][protocol][port]["state"]
                service = scanner[host][protocol][port].get("name", "unknown")

                if state == "open":
                    print(f"{Fore.GREEN}[✓] Port {port} open → {service}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[✗] Port {port} {state}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error scanning ports: {e}{Style.RESET_ALL}")