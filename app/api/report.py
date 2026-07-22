from fastapi import APIRouter, Request, Depends

from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.post("/generate")
def generate_report(
    request: Request,
    user=Depends(get_current_user),
):

    report_service = request.app.state.report_service
    servers = request.app.state.servers

    pdf = report_service.generate_report(servers)

    return {
        "message": "Report generated.",
        "path": str(pdf),
    }