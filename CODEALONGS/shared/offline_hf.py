"""Small shared runtime for local Hugging Face LlamaIndex examples."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata


@lru_cache(maxsize=None)
def load_text_model(model_dir: str):
    """Load one local causal model and tokenizer per model directory."""

    from transformers import AutoModelForCausalLM, AutoTokenizer

    path = Path(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(path, local_files_only=True).eval()
    return tokenizer, model


def generate_chat(model_dir: str, messages: list[dict[str, str]], max_new_tokens: int) -> str:
    """Generate deterministically from local Hugging Face weights."""

    tokenizer, model = load_text_model(model_dir)
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(
        output[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True
    ).strip()


class LocalHuggingFaceLLM(CustomLLM):
    """Minimal LlamaIndex LLM backed by a local Hugging Face chat model."""

    model_dir: str
    model_name: str = "local-hugging-face-model"
    max_new_tokens: int = 64
    generation_count: int = 0

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=2048,
            num_output=self.max_new_tokens,
            is_chat_model=True,
            model_name=self.model_name,
        )

    def generate_messages(self, messages: list[dict[str, str]]) -> str:
        text = generate_chat(self.model_dir, messages, self.max_new_tokens)
        self.generation_count += 1
        return text

    def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
        return CompletionResponse(text=self.generate_messages([{"role": "user", "content": prompt}]))

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs):
        yield self.complete(prompt, formatted=formatted, **kwargs)
