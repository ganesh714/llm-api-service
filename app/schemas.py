from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The input text for the LLM")
    max_new_tokens: int = Field(50, ge=1, le=200, description="Max tokens to generate")

class GenerateResponse(BaseModel):
    generated_text: str