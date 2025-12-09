import os
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.concurrency import run_in_threadpool
from app.schemas import GenerateRequest, GenerateResponse
from app.model import llm_engine

app = FastAPI(title="GPP LLM Microservice")

# Security: Load API Key from Environment Variable
API_KEY = os.getenv("API_KEY", "default-secret-key")

async def verify_api_key(x_api_key: str = Header(...)):
    """Dependency to validate the API key header."""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "LLM-Generator"}

@app.post("/generate", response_model=GenerateResponse, dependencies=[Depends(verify_api_key)])
async def generate(request: GenerateRequest):
    try:
        # CRITICAL: We run the CPU-bound inference in a threadpool
        # This keeps the main event loop free to handle other requests (like /health)
        result = await run_in_threadpool(
            llm_engine.generate_text, 
            request.prompt, 
            request.max_new_tokens
        )
        return {"generated_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))