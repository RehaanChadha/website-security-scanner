import unittest
from unittest.mock import patch

from services.scan_service import normalize_target, run_scan


class NormalizeTargetTests(unittest.TestCase):
    def test_normalize_adds_https_scheme(self):
        normalized = normalize_target("github.com")

        self.assertEqual(normalized["url"], "https://github.com")
        self.assertEqual(normalized["base_url"], "https://github.com")
        self.assertEqual(normalized["hostname"], "github.com")

    def test_normalize_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            normalize_target("   ")

    def test_normalize_rejects_unsupported_scheme(self):
        with self.assertRaises(ValueError):
            normalize_target("ftp://example.com")


class RunScanTests(unittest.TestCase):
    @patch("services.scan_service.scan_vulnerabilities")
    @patch("services.scan_service.scan_ssl")
    @patch("services.scan_service.scan_ports")
    @patch("services.scan_service.scan_headers")
    def test_run_scan_returns_completed_status(
        self,
        mock_headers,
        mock_ports,
        mock_ssl,
        mock_vulnerabilities,
    ):
        mock_headers.return_value = {
            "status_code": 200,
            "headers_found": ["Content-Security-Policy"],
            "headers_missing": ["Permissions-Policy"],
        }
        mock_ports.return_value = {
            "open_ports": [{"port": 443, "service": "https"}]
        }
        mock_ssl.return_value = {
            "issuer": "Test CA",
            "expiry_date": "2026-06-03 23:59:59",
            "days_remaining": 83,
        }
        mock_vulnerabilities.return_value = {
            "https_used": True,
            "server_header": "hidden",
            "x_powered_by": "hidden",
            "interesting_paths": [],
            "final_url": "https://github.com/",
        }

        report = run_scan("github.com", verbose=False)

        self.assertEqual(report["report_data"]["status"], "completed")
        self.assertIn("Completed successfully", report["report_text"])
        mock_headers.assert_called_once_with("https://github.com", verbose=False)
        mock_ports.assert_called_once_with("github.com", verbose=False)

    @patch("services.scan_service.scan_vulnerabilities")
    @patch("services.scan_service.scan_ssl")
    @patch("services.scan_service.scan_ports")
    @patch("services.scan_service.scan_headers")
    def test_run_scan_keeps_partial_results_when_one_scan_fails(
        self,
        mock_headers,
        mock_ports,
        mock_ssl,
        mock_vulnerabilities,
    ):
        mock_headers.return_value = {
            "status_code": 200,
            "headers_found": [],
            "headers_missing": ["Content-Security-Policy"],
        }
        mock_ports.return_value = {
            "open_ports": [],
            "error": "Nmap is not installed or not available on the server. Port scanning is unavailable.",
        }
        mock_ssl.return_value = {
            "issuer": "Test CA",
            "expiry_date": "2026-06-03 23:59:59",
            "days_remaining": 83,
        }
        mock_vulnerabilities.return_value = {
            "https_used": True,
            "server_header": "hidden",
            "x_powered_by": "hidden",
            "interesting_paths": [],
            "final_url": "https://github.com/",
        }

        report = run_scan("github.com", verbose=False)

        self.assertEqual(report["report_data"]["status"], "completed_with_errors")
        self.assertEqual(
            report["report_data"]["results"]["port_scan"]["error"],
            "Nmap is not installed or not available on the server. Port scanning is unavailable.",
        )
        self.assertIn("Completed with errors", report["report_text"])


if __name__ == "__main__":
    unittest.main()
