from fastapi import FastAPI, Query
from app.agent_ochestration import build_pipeline

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
    limit: int = Query(5, ge=1, le=50, description="Number of papers to return (1-50)")
):
    result = build_pipeline(query,limit)
    return result