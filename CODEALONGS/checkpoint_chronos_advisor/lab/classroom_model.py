"""Supplied mock tool-call model so the 135M lab stays reliable.

It represents the shape a stronger local model would return. Students build
the application around it; they do not need to implement model tool JSON.
"""

from smolagents import Model
from smolagents.models import ChatMessage, ChatMessageToolCall, ChatMessageToolCallFunction, MessageRole


class ClassroomModel(Model):
    """Return three predictable tool-call-shaped responses for this lab."""

    def __init__(self):
        super().__init__()
        self.calls = 0

    def generate(self, messages, tools_to_call_from=None, **kwargs):
        self.calls += 1
        if self.calls == 1:
            name, arguments = "portfolio_summary", {"client_id": "alice"}
        elif self.calls == 2:
            name, arguments = "policy_rag", {"query": "concentration limit"}
        else:
            name, arguments = "final_answer", {"answer": "Alice's portfolio and policy evidence were retrieved."}
        call = ChatMessageToolCall(
            id=str(self.calls),
            type="function",
            function=ChatMessageToolCallFunction(name=name, arguments=arguments),
        )
        return ChatMessage(role=MessageRole.ASSISTANT, tool_calls=[call])
