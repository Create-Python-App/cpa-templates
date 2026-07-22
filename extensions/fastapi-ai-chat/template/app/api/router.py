"""Application API router with health + chat features."""

from fastapi import APIRouter

from app.features.chat.router import router as chat_router
from app.features.health.router import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(chat_router)
