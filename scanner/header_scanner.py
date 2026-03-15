import requests
from colorama import Fore, Style


def scan_headers(url, verbose=True):
    results = {
        "status_code": None,
        "headers_found": [],
        "headers_missing": []
    }

    def log(message):
        if verbose:
            print(message)

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        status_code = response.status_code

        results["status_code"] = status_code

        log(f"\n{Fore.CYAN}Scanning Security Headers for: {url}{Style.RESET_ALL}")
        log(f"{Fore.CYAN}HTTP Status Code: {status_code}{Style.RESET_ALL}\n")

        security_headers = {
            "Content-Security-Policy": "Protects against XSS attacks",
            "Strict-Transport-Security": "Forces HTTPS connections",
            "X-Frame-Options": "Prevents clickjacking",
            "X-Content-Type-Options": "Prevents MIME sniffing",
            "Referrer-Policy": "Controls referrer information",
            "Permissions-Policy": "Controls browser features",
        }

        for header, description in security_headers.items():
            if header in headers:
                log(f"{Fore.GREEN}[✓] {header} found{Style.RESET_ALL}")
                results["headers_found"].append(header)
            else:
                log(f"{Fore.RED}[✗] {header} missing → {description}{Style.RESET_ALL}")
                results["headers_missing"].append(header)

    except requests.exceptions.RequestException as e:
        log(f"{Fore.RED}Error scanning site: {e}{Style.RESET_ALL}")
        results["error"] = str(e)

    return results
