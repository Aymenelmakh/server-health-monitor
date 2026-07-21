from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.server import Server
from app.services.email import EmailService


class ReportService:
    template_env : Environment
    email : EmailService

    def __init__(self, email):
        self.template_env = Environment(
            loader=FileSystemLoader("app/templates")
        )
        self.email = email

    def generate_report(self, servers: list[Server]):
        """
        Main function called by the scheduler.
        """
        summary = self._build_summary(servers)
        template = self.template_env.get_template("report.html")
        for s in servers:
            if s.status == "ONLINE":
                print(vars(s.metrics.security))
        html = template.render(
            servers=servers,
            summary=summary,
            generated_at=datetime.now()
        )
        output = Path("reports")
        output.mkdir(exist_ok=True)
        pdf_path = output / f"report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        HTML(string=html).write_pdf(pdf_path)

        # send email
        self.email.send_report(pdf_path, servers)
        return pdf_path
    
    def _build_summary(self, servers):
        summary = {
            "total": len(servers),
            "healthy": 0,
            "warning": 0,
            "critical": 0,
            "offline": 0,
            "average_cpu": 0,
            "average_ram": 0,
            "average_disk": 0,
        }
        cpu = []
        ram = []
        disk = []
        for server in servers:
            if server.status != "ONLINE":
                summary["offline"] += 1
                continue
            health = server.metrics.health_status()
            if health.name == "HEALTHY":
                summary["healthy"] += 1
            elif health.name == "WARNING":
                summary["warning"] += 1
            elif health.name == "CRITICAL":
                summary["critical"] += 1
            cpu.append(server.metrics.cpu.cpu_percent)
            ram.append(server.metrics.memory.ram_stats["percent"])
            disk.append(
                max(
                    usage["percent"]
                    for usage in server.metrics.disk.disk_usage.values()
                )
            )

        if cpu:
            summary["average_cpu"] = round(sum(cpu)/len(cpu),1)
        if ram:
            summary["average_ram"] = round(sum(ram)/len(ram),1)
        if disk:
            summary["average_disk"] = round(sum(disk)/len(disk),1)
        return summary