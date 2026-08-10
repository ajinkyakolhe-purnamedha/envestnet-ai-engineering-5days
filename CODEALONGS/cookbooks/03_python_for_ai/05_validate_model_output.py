# Validate model output
from pydantic import BaseModel

class ModelOutput(BaseModel):
    summary: str
    grounded: bool

output = ModelOutput.model_validate({"summary": "Cash remains above the limit.", "grounded": True})
print(output)

