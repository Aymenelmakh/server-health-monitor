from fastapi import APIRouter, HTTPException,Request, status
from pydantic import BaseModel, EmailStr, Field

from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    request: Request,
):
    auth_service = request.app.state.auth_service

    token = auth_service.login(
        credentials.email,
        credentials.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return LoginResponse(
        access_token=token,
    )