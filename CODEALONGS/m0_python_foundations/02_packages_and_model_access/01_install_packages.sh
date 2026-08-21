# Create a project once, then add only the library your feature needs.
uv init wealth-demo
cd wealth-demo

uv add fastapi uvicorn
uv add transformers torch
uv add google-genai
uv add python-dotenv 
uv add openai anthropic boto3
