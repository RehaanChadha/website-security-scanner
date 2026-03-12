from datetime import datetime
import os
import json


def save_report(domain, report_text):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/{domain}_scan_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(report_text)

    return filename


def save_json_report(domain, report_data):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/{domain}_scan_{timestamp}.json"

    with open(filename, "w") as file:
        json.dump(report_data, file, indent=4)

    return filename