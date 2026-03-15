# Website Security Scanner

A full-stack cybersecurity project that scans websites for common security misconfigurations and presents the results through both a Flask web app and a Python CLI.

## Live Demo

`https://website-security-scanner-fmbz.onrender.com`

## Overview

This project was built to showcase practical web security tooling concepts in a portfolio-ready format. It combines multiple scanner modules into one experience that can:

- analyze HTTP security headers
- inspect SSL/TLS certificate details
- detect open ports with `nmap`
- perform lightweight exposure checks
- generate structured scan results for both terminal and web use

The application is designed as a modular Python project with a shared scan service powering both interfaces.

## Features

- Flask-based web interface for browser-driven scanning
- Python CLI for local terminal usage
- Shared orchestration layer for consistent scan results
- Partial-failure handling so one failed module does not break the full scan
- Text and JSON report generation
- Render deployment using Docker

## Tech Stack

- Python
- Flask
- Requests
- `python-nmap`
- HTML / CSS
- Gunicorn
- Docker
- Render

## How It Works

The scan flow is organized around a shared service layer:

1. A target URL or hostname is submitted.
2. The target is normalized and validated.
3. The scanner runs:
   - security header analysis
   - port scanning
   - SSL inspection
   - vulnerability/exposure checks
4. Results are combined into one structured response.
5. The response is rendered in the web UI or exported through the CLI report flow.

## Project Structure

```text
website-security-scanner/
├── app.py
├── main.py
├── requirements.txt
├── Dockerfile
├── render.yaml
├── scanner/
│   ├── header_scanner.py
│   ├── port_scanner.py
│   ├── ssl_scanner.py
│   └── vulnerability_scanner.py
├── services/
│   └── scan_service.py
├── static/
├── templates/
├── tests/
├── utils/
│   └── report_generator.py
└── reports/
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/RehaanChadha/website-security-scanner.git
cd website-security-scanner
```

### 2. Create a virtual environment

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install `nmap`

Mac:

```bash
brew install nmap
```

Linux:

```bash
sudo apt install nmap
```

Windows:

Download and install `nmap` from:

`https://nmap.org/download.html`

## Run Locally

### Web App

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

### CLI

```bash
python3 main.py --target github.com
```

## Deployment

This project is deployed on Render and includes:

- `Dockerfile` for containerized deployment
- `render.yaml` for Render blueprint setup
- `gunicorn` as the production application server

## Testing

Run the test suite with:

```bash
venv/bin/python -m unittest discover -s tests
```

## Notes

- Port scanning depends on `nmap` being installed on the host environment.
- Some targets may block or rate-limit requests.
- This tool is intended for educational and authorized testing only.

## Author

Rehaan Chadha
