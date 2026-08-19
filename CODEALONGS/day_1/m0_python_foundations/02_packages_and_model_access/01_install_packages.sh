# Create a project once, then add only the library your feature needs.
uv init wealth-demo
cd wealth-demo

uv add fastapi uvicorn
uv add openai anthropic google-genai
uv add transformers diffusers
uv add python-dotenv 

