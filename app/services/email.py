import os
import smtplib
from datetime import datetime
from pathlib import Path
from email.message import EmailMessage

from app.models.server import Server


class EmailService:
    """
    Handles building and sending the daily report email (with the PDF
    attached) using settings from config.yaml's `email:` section and
    SMTP credentials from environment variables (.env).
    """

    enabled: bool
    sender_name: str
    recipients: list[str]
    subject: str
    attach_pdf: bool

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str

    def __init__(self, email_config: dict):
        self.enabled = email_config.get("enabled", False)
        self.sender_name = email_config.get("sender_name", "Server Monitoring System")
        self.recipients = email_config.get("recipients", [])
        self.subject = email_config.get("subject", "Server Health Report")
        self.attach_pdf = email_config.get("attach_pdf", True)

        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")

    def is_ready(self) -> bool:
        """
        Checks that email sending is enabled and all required settings
        (recipients + SMTP credentials) are present before attempting to send.
        """
        if not self.enabled:
            return False
        if not self.recipients:
            print("[email] No recipients configured, skipping send.")
            return False
        if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_pass]):
            print("[email] Missing SMTP credentials in environment, skipping send.")
            return False
        return True

    def send_report(self, pdf_path: Path, servers: list[Server] | None = None) -> bool:
        """
        Main entry point called by the scheduler after the PDF report
        has been generated. Returns True on success, False otherwise
        (never raises, so it can't crash the scheduler job).
        """
        if not self.is_ready():
            return False

        try:
            msg = self._build_message(pdf_path, servers)
            self._send(msg)
            print(f"[{datetime.now()}] Report emailed to {len(self.recipients)} recipient(s).")
            return True
        except smtplib.SMTPAuthenticationError:
            print(f"[{datetime.now()}] Email failed: SMTP authentication rejected (check SMTP_USER/SMTP_PASS).")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"[{datetime.now()}] Email failed: server refused recipients {e.recipients}.")
        except smtplib.SMTPConnectError:
            print(f"[{datetime.now()}] Email failed: could not connect to {self.smtp_host}:{self.smtp_port}.")
        except smtplib.SMTPException as e:
            print(f"[{datetime.now()}] Email failed: {e}")
        except FileNotFoundError:
            print(f"[{datetime.now()}] Email failed: PDF not found at {pdf_path}.")
        except Exception as e:
            print(f"[{datetime.now()}] Email failed: unexpected error - {e}")

        return False

    def _build_message(self, pdf_path: Path, servers: list[Server] | None) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = f"{self.sender_name} <{self.smtp_user}>"
        msg["To"] = ", ".join(self.recipients)

        msg.set_content(self._build_plain_body(servers))
        msg.add_alternative(self._build_html_body(servers), subtype="html")

        if self.attach_pdf:
            self._attach_pdf(msg, pdf_path)

        return msg

    def _attach_pdf(self, msg: EmailMessage, pdf_path: Path):
        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=pdf_path.name,
            )

    def _build_plain_body(self, servers: list[Server] | None) -> str:
        lines = [
            "Daily Datacenter Health Report",
            "",
            "Please find the full report attached as a PDF.",
            "",
        ]
        if servers:
            lines.append("Summary:")
            for server in servers:
                lines.append(f"  - {server.name}: {self._status_label(server)}")
        return "\n".join(lines)

    def _build_html_body(self, servers: list[Server] | None) -> str:
        rows = ""
        if servers:
            for server in servers:
                label = self._status_label(server)
                color = self._status_color(server)
                rows += (
                    f'<tr>'
                    f'<td style="padding:6px 10px;">{server.name}</td>'
                    f'<td style="padding:6px 10px;">'
                    f'<b style="color:{color};">{label}</b>'
                    f'</td>'
                    f'</tr>'
                )

        summary_table = ""
        if rows:
            summary_table = f"""
            <table style="border-collapse:collapse; margin-top:12px;">
                <tr>
                    <th style="text-align:left; padding:6px 10px; background:#12315c; color:#fff;">Server</th>
                    <th style="text-align:left; padding:6px 10px; background:#12315c; color:#fff;">Status</th>
                </tr>
                {rows}
            </table>
            """

        return f"""
        <html>
            <body style="font-family:Arial, sans-serif; color:#22303f;">
                <h2 style="color:#12315c;">Daily Datacenter Health Report</h2>
                <p>Please find the full report attached as a PDF.</p>
                {summary_table}
                <p style="margin-top:16px; font-size:12px; color:#8a94a3;">
                    T-Man Casablanca Group &bull; Server Monitoring System
                </p>
            </body>
        </html>
        """

    def _status_label(self, server: Server) -> str:
        if server.status != "ONLINE":
            return "OFFLINE"
        health = server.metrics.health_status()
        return health.name

    def _status_color(self, server: Server) -> str:
        if server.status != "ONLINE":
            return "#d8453f"
        health = server.metrics.health_status().name
        return {
            "HEALTHY": "#22a35c",
            "WARNING": "#e8912b",
            "CRITICAL": "#d8453f",
        }.get(health, "#8a94a3")

    def _send(self, msg: EmailMessage):
        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as smtp:
            smtp.login(self.smtp_user, self.smtp_pass)
            smtp.send_message(msg)