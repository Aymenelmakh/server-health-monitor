from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from time import sleep

from app.services.collector import CollectorService
from app.services.report import ReportService
from app.models.server import Server

class SchedulerService:
    collector:CollectorService
    Servers:list[Server]
    scheduler:BackgroundScheduler
    report:ReportService

    def __init__(self, collector, servers, report):
        self.collector = collector
        self.servers = servers
        self.scheduler = BackgroundScheduler()
        self.report = report
    
    def _collect_job(self):
        self.collector.collect_all_servers(self.servers)
    
    def _daily_report_job(self):
        self.report.generate_report(self.servers)

    def start(self):
        # collect every second
        self.scheduler.add_job(
            self._collect_job, 
            trigger = "interval", 
            seconds=10
        )

        # Every day at 08:00
        self.scheduler.add_job(
            self._daily_report_job,
            trigger="cron",
            hour=11,
            minute=42
        )

        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()