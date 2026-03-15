import argparse
from colorama import Fore, Style, init
from services.scan_service import normalize_target, run_scan
from utils.report_generator import save_report, save_json_report

init(autoreset=True)


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

    print(f"\n{Fore.YELLOW}Starting scan for: {target['url']}{Style.RESET_ALL}")

    report = run_scan(args.target, verbose=True)
    report_data = report["report_data"]
    report_text = report["report_text"]

    report_file = save_report(target["report_name"], report_text)
    json_report_file = save_json_report(target["report_name"], report_data)

    print(f"\n{Fore.GREEN}Text report saved to: {report_file}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}JSON report saved to: {json_report_file}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
