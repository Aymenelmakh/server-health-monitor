from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml

from app.models.server import Server
from app.services.auth import AuthService
from app.services.collector import CollectorService
from app.services.email import EmailService
from app.services.report import ReportService
from app.services.scheduler import SchedulerService

from app.api.auth import router as auth_router
from app.api.dashboard import router as server_router
# from app.api.report import router as report_router


def load_servers(config_path: str) -> list[Server]:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return [
        Server.from_dict(server_data)
        for server_data in config["servers"]
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting Server Monitoring Backend...")

    load_dotenv()

    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Create services
    auth_service = AuthService()
    email_service = EmailService(config["email"])
    collector_service = CollectorService()
    report_service = ReportService(email_service)

    # Load servers
    servers = load_servers("config/config.yaml")

    # Create scheduler
    scheduler_service = SchedulerService(
        collector_service,
        servers,
        report_service,
    )

    scheduler_service.start()

    # Share objects with the whole application
    app.state.auth_service = auth_service
    app.state.email_service = email_service
    app.state.collector_service = collector_service
    app.state.report_service = report_service
    app.state.scheduler_service = scheduler_service
    app.state.servers = servers

    print("Scheduler started.")

    yield

    print("Stopping scheduler...")

    scheduler_service.stop()

    print("Backend stopped.")


app = FastAPI(
    title="Server Monitoring API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(server_router)
# app.include_router(report_router)