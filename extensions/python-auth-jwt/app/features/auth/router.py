"""Auth router skeleton — mount from your API router when ready."""

from fastapi import APIRouter, HTTPException, status

from app.features.auth.schemas import LoginRequest, TokenResponse, UserPublic
from app.features.auth.service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# Demo-only in-memory user. Replace with your persistence layer.
_DEMO_EMAIL = "demo@example.com"
_DEMO_HASH = hash_password("password123")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    if body.email != _DEMO_EMAIL or not verify_password(body.password, _DEMO_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return TokenResponse(access_token=create_access_token(body.email))


@router.get("/me", response_model=UserPublic)
def me() -> UserPublic:
    return UserPublic(email=_DEMO_EMAIL)
