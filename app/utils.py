"""
Utility functions for PDF conversion using wkhtmltopdf.
"""

import subprocess


def convert_html_to_pdf(html: str) -> bytes:
    """
    Convert HTML content to PDF bytes using the wkhtmltopdf CLI.
    """
    process = subprocess.run(
        ["wkhtmltopdf", "-", "-"],
        input=html.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if process.returncode != 0:
        error_message = process.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"wkhtmltopdf failed with code {process.returncode}: {error_message}"
        )

    return process.stdout
