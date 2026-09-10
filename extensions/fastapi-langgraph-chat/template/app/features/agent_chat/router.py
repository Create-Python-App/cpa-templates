"""Agent chat HTTP routes (multi-step LangGraph orchestration)."""

from fastapi import APIRouter, Request

from app.features.agent_chat.schemas import AgentChatRequest, AgentChatResponse
from app.features.agent_chat.service import agent_chat_completion
from app.schemas.common.responses import APIResponse, make_item_response

router = APIRouter(prefix="/agent/chat", tags=["agent-chat"])


@router.post("", response_model=APIResponse[AgentChatResponse])
def create_agent_chat(
    body: AgentChatRequest, request: Request
) -> APIResponse[AgentChatResponse]:
    result = agent_chat_completion(body)
    return make_item_response(
        data=result,
        dev_code="AGENT_CHAT_COMPLETED",
        message="Agent chat completion generated",
        request_id=getattr(request.state, "request_id", "unknown"),
    )
