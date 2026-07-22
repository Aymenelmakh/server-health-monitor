from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get("/servers")
def get_servers(
    request: Request,
    user=Depends(get_current_user),
):
    servers = request.app.state.servers

    return servers