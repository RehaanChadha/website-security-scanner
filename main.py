from scanner.header_scanner import scan_headers


def main():
    url = input("Enter website URL (example: https://example.com): ")

    if not url.startswith("http"):
        url = "https://" + url

    scan_headers(url)


if __name__ == "__main__":
    main()