"""Chat HTTP routes."""

from fastapi import APIRouter

from app.features.chat.schemas import ChatRequest, ChatResponse
from app.features.chat.service import chat_completion

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def create_chat(body: ChatRequest) -> ChatResponse:
    return chat_completion(body)
