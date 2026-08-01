"""CORS initialization helper (fastapi-cors extension)."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    """Register CORS middleware if origins are configured."""
    origins_str = os.getenv("CORS_ORIGINS", "").strip()
    if not origins_str:
        return

    origins = [origin.strip() for origin in origins_str.split(",") if origin.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
