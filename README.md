# Website Security Scanner

A **modular Python-based cybersecurity tool** that scans websites for common security misconfigurations and exposure risks through both a **CLI** and a **Flask web app**.

The scanner performs multiple checks including:

- HTTP security header analysis
- Port scanning with Nmap
- SSL/TLS certificate inspection
- Basic vulnerability reconnaissance
- Automated security report generation
- Browser-based scan results with a responsive dashboard

This project demonstrates practical security tooling concepts used in **real-world reconnaissance and vulnerability assessment workflows**.

---

## Features

### Security Header Analysis

Detects missing or misconfigured HTTP security headers that protect against common attacks.

Examples:

- Content Security Policy
- HSTS (Strict Transport Security)
- Clickjacking protection
- MIME sniffing protection

Example output:

```text
[✓] Content-Security-Policy found
[✓] Strict-Transport-Security found
[✓] X-Frame-Options found
[✗] Permissions-Policy missing
```

### Port Scanning

Identifies open ports and exposed services using Nmap integration.

Example findings:

```text
Port 22 → SSH
Port 80 → HTTP
Port 443 → HTTPS
```

### SSL/TLS Inspection

Analyzes SSL certificates to detect potential configuration issues.

Checks include:

- Certificate issuer
- Expiration date
- Remaining validity period

Example:

```text
Certificate Issuer: Sectigo Limited
Certificate Expiry: 2026-06-03
Days Remaining: 83
```

### Basic Vulnerability Reconnaissance

Performs lightweight reconnaissance checks including:

- HTTPS usage verification
- Exposed server headers
- Technology fingerprinting
- Discovery of potentially sensitive paths

Examples:

```text
/backup
/config
/test
```

These findings represent potential exposure points, not confirmed vulnerabilities.

### Automated Reporting

The scanner automatically generates two report formats.

Text report:

```text
reports/github.com_scan_YYYY-MM-DD_HH-MM-SS.txt
```

JSON report:

```text
reports/github.com_scan_YYYY-MM-DD_HH-MM-SS.json
```

### Web Dashboard

The project now includes a Flask-powered web interface with:

- A landing page and scan form
- In-browser results for headers, ports, SSL, and exposure checks
- Clear partial-failure handling when one scan module errors
- A `/health` endpoint for deployment checks

## Technologies Used

Python libraries:

- `requests`
- `python-nmap`
- `colorama`
- `Flask`
- `ssl` / `socket`
- `argparse`
- `urllib.parse`

External tools:

- `nmap`

## Installation

### Clone the repository

```bash
git clone https://github.com/RehaanChadha/website-security-scanner.git
cd website-security-scanner
```

### Create a virtual environment

Mac / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Nmap

The scanner requires Nmap for port scanning.

Mac:

```bash
brew install nmap
```

Linux:

```bash
sudo apt install nmap
```

Windows:

Download and install Nmap from:

`https://nmap.org/download.html`

Choose the installer:

`nmap-setup.exe`

During installation, make sure `Add Nmap to PATH` is selected.

Verify installation:

```bash
nmap --version
```

## Running the Web App

Start the Flask app:

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Available routes:

- `GET /` → landing page and scan form
- `POST /scan` → run a scan and render results
- `GET /health` → health check JSON response

## Running the CLI

Run the original CLI scanner:

```bash
python3 main.py --target github.com
```

The CLI and the web app both use the same shared scan orchestration logic.

## Usage

Run the scanner from the command line:

```bash
python3 main.py --target github.com
```

## Example Output

```text
Starting scan for: https://github.com

Scanning Security Headers for: https://github.com
HTTP Status Code: 200

[✓] Content-Security-Policy found
[✓] Strict-Transport-Security found
[✓] X-Frame-Options found
[✗] Permissions-Policy missing

Scanning Open Ports for: github.com

[✓] Port 22 open → ssh
[✓] Port 80 open → http
[✓] Port 443 open → https

Scanning SSL/TLS for: github.com

Certificate Issuer: Sectigo Limited
Certificate Expiry: 2026-06-03 23:59:59
Days Remaining: 83 days
```

## Project Structure

```text
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
```

## Educational Purpose

This tool is intended for educational and research purposes only.

Only scan systems you own or have permission to test.

Unauthorized scanning may violate laws or organizational policies.

## Author

Rehaan Chadha  
Business Technology Management  
Toronto Metropolitan University
