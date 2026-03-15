import ssl
import socket
from datetime import datetime
from colorama import Fore, Style


def scan_ssl(domain, verbose=True):
    results = {
        "issuer": None,
        "expiry_date": None,
        "days_remaining": None
    }

    def log(message):
        if verbose:
            print(message)

    try:
        log(f"\n{Fore.CYAN}Scanning SSL/TLS for: {domain}{Style.RESET_ALL}\n")

        context = ssl.create_default_context()

        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cert = secure_sock.getpeercert()

        issuer = dict(x[0] for x in cert["issuer"])
        issued_by = issuer.get("organizationName", "Unknown")

        expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry_date - datetime.utcnow()).days

        results["issuer"] = issued_by
        results["expiry_date"] = str(expiry_date)
        results["days_remaining"] = days_left

        log(f"{Fore.GREEN}Certificate Issuer:{Style.RESET_ALL} {issued_by}")
        log(f"{Fore.GREEN}Certificate Expiry:{Style.RESET_ALL} {expiry_date}")
        log(f"{Fore.GREEN}Days Remaining:{Style.RESET_ALL} {days_left} days")

        if days_left < 30:
            log(f"{Fore.RED}Certificate expiring soon!{Style.RESET_ALL}")

    except Exception as e:
        log(f"{Fore.RED}Error scanning SSL: {e}{Style.RESET_ALL}")
        results["error"] = str(e)

    return results
