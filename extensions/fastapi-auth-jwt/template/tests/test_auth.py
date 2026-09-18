"""Tests for fastapi-auth-jwt extension (password hashing, JWT, router)."""

from __future__ import annotations

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.features.auth.router import router as auth_router
from app.features.auth.schemas import LoginRequest, TokenResponse, UserPublic
from app.features.auth.service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------


def test_hash_and_verify_roundtrip() -> None:
    password = "s3cur3-P@ssw0rd!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_hash_is_salted() -> None:
    password = "password123"
    first = hash_password(password)
    second = hash_password(password)
    # Argon2 uses a random salt, so hashes must differ.
    assert first != second
    assert verify_password(password, first) is True
    assert verify_password(password, second) is True


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------


def test_create_and_decode_token_roundtrip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "test-secret-for-unit-tests-32-chars")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_EXPIRE_MINUTES", "60")
    token = create_access_token("user@example.com")
    assert isinstance(token, str)
    assert token.count(".") == 2  # JWT header.payload.signature
    payload = decode_access_token(token)
    assert payload["sub"] == "user@example.com"
    assert "exp" in payload


def test_create_token_with_extra_claims(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "test-secret-extra-32-chars-long!!")
    token = create_access_token("user@example.com", extra={"role": "admin"})
    payload = decode_access_token(token)
    assert payload["sub"] == "user@example.com"
    assert payload["role"] == "admin"


def test_token_respects_algorithm_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "hs256-secret-32-chars-long-for-test!!")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    token = create_access_token("a@b.co")
    header = jwt.get_unverified_header(token)
    assert header["alg"] == "HS256"


def test_token_invalid_after_secret_change(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JWT_SECRET", "first-secret-32-chars-long-for-test!!")
    token = create_access_token("a@b.co")
    monkeypatch.setenv("JWT_SECRET", "different-secret-32-chars-long-test!!")
    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(token)


def test_token_expiry_is_future(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import UTC, datetime

    monkeypatch.setenv("JWT_SECRET", "expiry-test-secret-32-chars-long!!")
    monkeypatch.setenv("JWT_EXPIRE_MINUTES", "60")
    before = datetime.now(UTC)
    token = create_access_token("a@b.co")
    payload = decode_access_token(token)
    exp_ts = payload["exp"]
    # exp is numeric timestamp; should be ~60 minutes after now.
    exp_dt = datetime.fromtimestamp(exp_ts, tz=UTC)
    delta = (exp_dt - before).total_seconds()
    assert 3500 < delta < 3700  # allow small clock drift


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------


def test_login_request_accepts_valid() -> None:
    req = LoginRequest(email="demo@example.com", password="password123")
    assert req.email == "demo@example.com"


def test_login_request_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email="demo@example.com", password="short")


def test_login_request_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password="password123")


def test_token_response_defaults_to_bearer() -> None:
    resp = TokenResponse(access_token="tok")
    assert resp.token_type == "bearer"
    assert resp.access_token == "tok"


def test_user_public_schema() -> None:
    user = UserPublic(email="demo@example.com")
    assert user.email == "demo@example.com"


# ---------------------------------------------------------------------------
# Router wiring
# ---------------------------------------------------------------------------


@pytest.fixture()
def auth_client() -> TestClient:
    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1")
    return TestClient(app)


def test_login_success_returns_token(
    auth_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Use a sufficiently long secret to avoid PyJWT InsecureKeyLengthWarning
    monkeypatch.setenv("JWT_SECRET", "w3-test-secret-32-chars-long-for-jwt!!")
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    # Token should decode to demo user
    payload = decode_access_token(body["access_token"])
    assert payload["sub"] == "demo@example.com"


def test_login_wrong_password_returns_401(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "wrongpass123"},
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.text


def test_login_wrong_email_returns_401(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "other@example.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_me_returns_demo_user(auth_client: TestClient) -> None:
    response = auth_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "demo@example.com"


def test_login_rejects_invalid_payload_shape(auth_client: TestClient) -> None:
    # Missing password triggers validation error (422 envelope via FastAPI)
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com"},
    )
    assert response.status_code == 422
