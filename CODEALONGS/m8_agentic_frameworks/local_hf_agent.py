"""LlamaIndex adapter for the local SmolLM2 function-calling model."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Sequence
import sys

from llama_index.core.base.llms.types import ChatMessage, ChatResponse, LLMMetadata, MessageRole
from llama_index.core.llms.llm import ToolSelection
from llama_index.core.tools import AsyncBaseTool


MODEL_DIR = Path(__file__).resolve().parents[2] / "OFFLINE-AI-Models" / "smollm2-1.7b-instruct"
SHARED_DIR = Path(__file__).resolve().parents[1] / "shared"
sys.path.insert(0, str(SHARED_DIR))

from offline_hf import LocalHuggingFaceLLM


TOOL_CALL_PATTERN = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL)


def require_m8_agent_model() -> Path:
    """Return the downloaded model directory or explain how to provision it."""

    if not (MODEL_DIR / "config.json").exists():
        raise FileNotFoundError(
            "M8 needs the local SmolLM2 model. Run: "
            "uv run --project CODEALONGS python "
            "CODEALONGS/m8_agentic_frameworks/download_local_models.py"
        )
    return MODEL_DIR


def tool_system_prompt(tools: Sequence[AsyncBaseTool]) -> str:
    schemas = [tool.metadata.to_openai_tool() for tool in tools]
    return (
        "You are an expert in composing functions. Based on the user's question, "
        "make one or more function calls to achieve the purpose. "
        "If no tool is useful, return an empty list.\n\n"
        "You have access to the following tools:\n"
        f"<tools>{json.dumps(schemas)}</tools>\n"
        "Your output must contain no text other than this exact format:\n"
        "<tool_call>[{\"name\": \"tool_name\", \"arguments\": {}}]</tool_call>"
    )


FINAL_ANSWER_SYSTEM_PROMPT = (
    "You are a helpful financial-assistant demo. The tool has already returned "
    "the required data. Give the user a concise final answer using that data. "
    "Do not call another tool and do not include tool-call tags."
)


class LocalSmolFunctionLLM(LocalHuggingFaceLLM):
    """A real local Hugging Face LLM with SmolLM2 tool-call parsing."""

    model_dir: str = str(MODEL_DIR)
    model_name: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=2048,
            num_output=192,
            is_chat_model=True,
            is_function_calling_model=True,
            model_name=self.model_name,
        )

    def _generate(self, messages: list[dict[str, str]]) -> str:
        require_m8_agent_model()
        return self.generate_messages(messages)

    def chat_with_tools(
        self,
        tools: Sequence[AsyncBaseTool],
        chat_history: list[ChatMessage] | None = None,
        **kwargs,
    ) -> ChatResponse:
        history = chat_history or []
        has_tool_result = any(message.role == MessageRole.TOOL for message in history)
        system_prompt = FINAL_ANSWER_SYSTEM_PROMPT if has_tool_result else tool_system_prompt(tools)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(
            {"role": message.role.value, "content": message.content or ""}
            for message in history
            if message.role != MessageRole.SYSTEM
        )
        return ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=self._generate(messages))
        )

    async def achat_with_tools(self, *args, **kwargs) -> ChatResponse:
        return await asyncio.to_thread(self.chat_with_tools, *args, **kwargs)

    def get_tool_calls_from_response(
        self, response: ChatResponse, error_on_no_tool_call: bool = True, **kwargs
    ) -> list[ToolSelection]:
        match = TOOL_CALL_PATTERN.search(response.message.content or "")
        if not match:
            if error_on_no_tool_call:
                raise ValueError("The local model did not return a tool call.")
            return []
        calls = json.loads(match.group(1))
        return [
            ToolSelection(
                tool_id=f"local-call-{index}",
                tool_name=call["name"],
                tool_kwargs=call.get("arguments", {}).get(
                    "properties", call.get("arguments", {})
                ),
            )
            for index, call in enumerate(calls)
        ]
