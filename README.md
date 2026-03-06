# Website Security Scanner

A Python-based cybersecurity tool that scans websites for common security issues.

## Features

- HTTP Security Header Analysis
- Port Scanning
- SSL/TLS Inspection
- Basic Vulnerability Detection
- Automated Security Reports

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Nmap
- Colorama

## Installation

Clone the repository:

git clone https://github.com/RehaanChadha/website-security-scanner.git
cd website-security-scanner

Create a virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Usage

Run the scanner:

python main.py

Enter a website URL when prompted.

Example:

github.com

## Example Output

Scanning Security Headers for: https://github.com
HTTP Status Code: 200

[✓] Content-Security-Policy found
[✓] Strict-Transport-Security found
[✓] X-Frame-Options found
[✓] X-Content-Type-Options found
[✓] Referrer-Policy found
[✗] Permissions-Policy missing

## Project Structure

website-security-scanner

│
├── main.py  
├── requirements.txt  
├── README.md  

├── scanner  
│   ├── header_scanner.py  
│   ├── port_scanner.py  
│   ├── ssl_scanner.py  
│   └── vulnerability_scanner.py  

├── utils  
├── reports  

## Author

Rehaan Chadha