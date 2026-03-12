# Website Security Scanner

A **modular Python-based cybersecurity tool** that scans websites for common security misconfigurations and exposure risks.

The scanner performs multiple checks including:

- HTTP security header analysis
- Port scanning with Nmap
- SSL/TLS certificate inspection
- Basic vulnerability reconnaissance
- Automated security report generation

This project demonstrates practical security tooling concepts used in **real-world reconnaissance and vulnerability assessment workflows**.

---

# Features

## Security Header Analysis

Detects missing or misconfigured HTTP security headers that protect against common attacks.

Examples:

- Content Security Policy
- HSTS (Strict Transport Security)
- Clickjacking protection
- MIME sniffing protection

Example output:


[✓] Content-Security-Policy found
[✓] Strict-Transport-Security found
[✓] X-Frame-Options found
[✗] Permissions-Policy missing


---

## Port Scanning

Identifies open ports and exposed services using **Nmap integration**.

Example findings:


Port 22 → SSH
Port 80 → HTTP
Port 443 → HTTPS


---

## SSL/TLS Inspection

Analyzes SSL certificates to detect potential configuration issues.

Checks include:

- Certificate issuer
- Expiration date
- Remaining validity period

Example:


Certificate Issuer: Sectigo Limited
Certificate Expiry: 2026-06-03
Days Remaining: 83


---

## Basic Vulnerability Reconnaissance

Performs lightweight reconnaissance checks including:

- HTTPS usage verification
- Exposed server headers
- Technology fingerprinting
- Discovery of potentially sensitive paths

Examples:


/backup
/config
/test


These findings represent **potential exposure points**, not confirmed vulnerabilities.

---

## Automated Reporting

The scanner automatically generates **two report formats**.

### Text Report

Human-readable scan report.


reports/github.com_scan_YYYY-MM-DD_HH-MM-SS.txt


### JSON Report

Structured report suitable for automation and security pipelines.


reports/github.com_scan_YYYY-MM-DD_HH-MM-SS.json


---

# Technologies Used

Python libraries:

- `requests`
- `python-nmap`
- `colorama`
- `ssl` / `socket`
- `argparse`
- `urllib.parse`

External tools:

- **Nmap**

---

# Installation

## Clone the repository

```bash
git clone https://github.com/RehaanChadha/website-security-scanner.git
cd website-security-scanner
Create a Virtual Environment
Mac / Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Install Nmap

The scanner requires Nmap for port scanning.

Mac
brew install nmap
Linux
sudo apt install nmap
Windows

Download and install Nmap from:

https://nmap.org/download.html

Choose the installer:

nmap-setup.exe

During installation make sure "Add Nmap to PATH" is selected.

Verify installation:

nmap --version
Usage

Run the scanner using the command-line interface.

python main.py --target github.com

You can also scan full URLs.

python main.py --target https://example.com
Example Output
Starting scan for: https://github.com

Scanning Security Headers...

[✓] Content-Security-Policy found
[✓] Strict-Transport-Security found
[✓] X-Frame-Options found
[✗] Permissions-Policy missing

Scanning Open Ports...

[✓] Port 22 open → ssh
[✓] Port 80 open → http
[✓] Port 443 open → https

Scanning SSL/TLS...

Certificate Issuer: Sectigo Limited
Certificate Expiry: 2026-06-03
Days Remaining: 83
Project Structure
website-security-scanner
│
├── main.py
├── requirements.txt
├── README.md
│
├── scanner
│   ├── header_scanner.py
│   ├── port_scanner.py
│   ├── ssl_scanner.py
│   └── vulnerability_scanner.py
│
├── utils
│   └── report_generator.py
│
└── reports
Educational Purpose

This tool is intended for educational and research purposes only.

Only scan systems you own or have permission to test.

Unauthorized scanning may violate laws or organizational policies.

Author

Rehaan Chadha

Business Technology Management
Toronto Metropolitan University

Future Improvements

Possible enhancements:

Advanced vulnerability detection

Subdomain discovery

Directory brute forcing

HTML report dashboard

Multi-target scanning

Integration with security APIs