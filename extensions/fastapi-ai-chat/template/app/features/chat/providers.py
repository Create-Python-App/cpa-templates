"""Chat model provider factory (langchain-core BaseChatModel).

Mock only in this MVP — a real provider gets wired via langchain's
init_chat_model() in a future issue, once one exists.
"""

from __future__ import annotations

import itertools

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

_MOCK_RESPONSE = "Hello! I'm a mock AI response. Set AI_CHAT_PROVIDER to use a real provider."


def get_provider(name: str) -> BaseChatModel:
    if name == "mock":
        return GenericFakeChatModel(messages=itertools.cycle([_MOCK_RESPONSE]))
    raise ValueError(f"unknown AI_CHAT_PROVIDER: {name!r} (only 'mock' is implemented in this MVP)")
