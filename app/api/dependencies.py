from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    auth_service = request.app.state.auth_service

    payload = auth_service.verify_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload