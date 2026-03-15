import unittest
from unittest.mock import patch

from app import create_app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Run security scan", response.data)

    @patch("app.run_scan")
    def test_scan_renders_results_for_valid_input(self, mock_run_scan):
        mock_run_scan.return_value = {
            "target": {
                "hostname": "github.com",
                "url": "https://github.com",
            },
            "report_data": {
                "target": "github.com",
                "url": "https://github.com",
                "status": "completed",
                "results": {
                    "header_scan": {
                        "status_code": 200,
                        "headers_found": ["Content-Security-Policy"],
                        "headers_missing": ["Permissions-Policy"],
                    },
                    "port_scan": {
                        "open_ports": [{"port": 443, "service": "https"}],
                    },
                    "ssl_scan": {
                        "issuer": "Test CA",
                        "expiry_date": "2026-06-03 23:59:59",
                        "days_remaining": 83,
                    },
                    "vulnerability_scan": {
                        "https_used": True,
                        "server_header": "hidden",
                        "x_powered_by": "hidden",
                        "interesting_paths": [],
                    },
                },
            },
            "report_text": "Website Security Scan Report",
        }

        response = self.client.post("/scan", data={"target": "github.com"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Completed successfully", response.data)
        self.assertIn(b"https://github.com", response.data)
        mock_run_scan.assert_called_once_with("github.com", verbose=False)

    @patch("app.run_scan")
    def test_scan_shows_validation_error_for_invalid_input(self, mock_run_scan):
        mock_run_scan.side_effect = ValueError("Enter a website URL or hostname to scan.")

        response = self.client.post("/scan", data={"target": ""})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Enter a website URL or hostname to scan.", response.data)

    @patch("app.run_scan")
    def test_scan_shows_partial_failure_results(self, mock_run_scan):
        mock_run_scan.return_value = {
            "target": {
                "hostname": "github.com",
                "url": "https://github.com",
            },
            "report_data": {
                "target": "github.com",
                "url": "https://github.com",
                "status": "completed_with_errors",
                "results": {
                    "header_scan": {
                        "status_code": 200,
                        "headers_found": [],
                        "headers_missing": ["Content-Security-Policy"],
                    },
                    "port_scan": {
                        "open_ports": [],
                        "error": "Port scanning is unavailable.",
                    },
                    "ssl_scan": {
                        "issuer": "Test CA",
                        "expiry_date": "2026-06-03 23:59:59",
                        "days_remaining": 83,
                    },
                    "vulnerability_scan": {
                        "https_used": True,
                        "server_header": "hidden",
                        "x_powered_by": "hidden",
                        "interesting_paths": [],
                    },
                },
            },
            "report_text": "Website Security Scan Report",
        }

        response = self.client.post("/scan", data={"target": "github.com"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Completed with errors", response.data)
        self.assertIn(b"Port scanning is unavailable.", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
