from scanner.header_scanner import scan_headers
from scanner.port_scanner import scan_ports


def main():
    url = input("Enter website URL (example: https://example.com): ")

    if not url.startswith("http"):
        url = "https://" + url

    scan_headers(url)
    scan_ports(url.replace("https://", "").replace("http://", ""))


if __name__ == "__main__":
    main()