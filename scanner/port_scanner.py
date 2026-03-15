import nmap
from colorama import Fore, Style


def scan_ports(target, verbose=True):
    results = {
        "open_ports": []
    }

    def log(message):
        if verbose:
            print(message)

    try:
        scanner = nmap.PortScanner()

        log(f"\n{Fore.CYAN}Scanning Open Ports for: {target}{Style.RESET_ALL}\n")

        scanner.scan(hosts=target, arguments="-F")

        if not scanner.all_hosts():
            log(f"{Fore.RED}No host found or target is unreachable.{Style.RESET_ALL}")
            results["error"] = "Host unreachable"
            return results

        host = scanner.all_hosts()[0]

        for protocol in scanner[host].all_protocols():
            ports = scanner[host][protocol].keys()

            for port in sorted(ports):
                state = scanner[host][protocol][port]["state"]
                service = scanner[host][protocol][port].get("name", "unknown")

                if state == "open":
                    log(f"{Fore.GREEN}[✓] Port {port} open → {service}{Style.RESET_ALL}")
                    results["open_ports"].append({
                        "port": port,
                        "service": service
                    })
                else:
                    log(f"{Fore.RED}[✗] Port {port} {state}{Style.RESET_ALL}")

    except Exception as e:
        log(f"{Fore.RED}Error scanning ports: {e}{Style.RESET_ALL}")
        error_text = str(e)
        if "nmap program was not found" in error_text.lower():
            error_text = (
                "Nmap is not installed or not available on the server. "
                "Port scanning is unavailable."
            )
        results["error"] = error_text

    return results
