"""A real, offline LlamaIndex agent that calls a local Hugging Face model."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4_building_rags"))

from llama_index.core import Settings
from llama_index.core.agent.workflow import ReActAgent

from workshop_llamaindex_setup import use_local_models


def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""

    return a * b


# This loads OFFLINE-AI-Models/smollm2-135m-instruct locally.
# It makes no API or internet request.
use_local_models()

agent = ReActAgent(
    tools=[multiply],
    llm=Settings.llm,
    system_prompt=(
        "You are a helpful calculator. For multiplication questions, respond "
        "in ReAct format and call the multiply tool before answering."
    ),
)


async def main() -> None:
    response = await agent.run("What is 12 multiplied by 7?")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
