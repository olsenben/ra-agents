from fastapi import FastAPI, Query, Depends, HTTPException, Header
from app.agent_ochestration import build_pipeline
import os

API_KEY = os.environ.get("FLY_API_TOKEN") 

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status" : "ok"}

@app.get("/analyze")
def analyze(
    query: str = Query(..., description="Research topic to Analyze"),
    limit: int = Query(5, ge=1, le=50, description="Number of papers to return (1-50)"),
    auth: None = Depends(verify_api_key)
):
    result = build_pipeline(query,limit)
    return result