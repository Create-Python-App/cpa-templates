"""Chat HTTP routes."""

from fastapi import APIRouter, Request

from app.features.chat.schemas import ChatRequest, ChatResponse
from app.features.chat.service import chat_completion
from app.schemas.common.responses import APIResponse, make_item_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=APIResponse[ChatResponse])
def create_chat(body: ChatRequest, request: Request) -> APIResponse[ChatResponse]:
    result = chat_completion(body)
    return make_item_response(
        data=result,
        dev_code="CHAT_COMPLETED",
        message="Chat completion generated",
        request_id=getattr(request.state, "request_id", "unknown"),
    )
