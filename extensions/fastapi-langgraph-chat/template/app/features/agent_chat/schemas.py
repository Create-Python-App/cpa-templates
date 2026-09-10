"""Agent chat request/response schemas."""

from pydantic import BaseModel, Field


class AgentChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1)


class AgentChatRequest(BaseModel):
    messages: list[AgentChatMessage] = Field(min_length=1)
    model: str | None = None


class AgentChatResponse(BaseModel):
    message: AgentChatMessage
    route: str
    provider: str
    model: str
