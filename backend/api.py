from fastapi import FastAPI, Query, Depends, HTTPException, Header, APIRouter
from agent_ochestration import build_pipeline
from schemas import AnalyzeQueryParams, RunOut 
from schemas import get_analyze_params, get_recent_runs, save_pipeline_run, delete_entry
from auth import verify_firebase_token, user_id_rate_limit_key
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import os
import aioredis


# API_KEY = os.environ.get("FLY_API_TOKEN") 

# def verify_api_key(x_api_key: str = Header(...)):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid API Key")

#get redis url from env
redis_url = os.environ.get("REDIS_URL")


#async context manager for connection to redis for rate limiting
@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = await aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis, identifier=user_id_rate_limit_key)

    yield #app runs here

    #shudown cleanup
    await redis.close()

#instantiate FastAPI with lifespan referencing contenxt manager
app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="0.1.0",
    lifespan=lifespan
)

#reusable rate limiter
rate_limit = Depends(RateLimiter(times=5, seconds=60))

#API router
router = APIRouter()

#API health check
@router.get("/health")
async def health_check():
    return {"status" : "ok"}

#route: run pipeline and save query 
@router.get("/analyze", dependencies=[rate_limit])
async def analyze(
    params: AnalyzeQueryParams = Depends(get_analyze_params), #verify input against input schema
    user = Depends(verify_firebase_token) #verify user token 
):
    result = build_pipeline(params.query,params.limit) #run query pipeline
    result['user_id'] = user['user_id'] #fron the authentification header we have unique user identifier
    save_pipeline_run(result) #save results to database
    return result

#route: retrieve previous queries per user
@router.get("/results", response_model=list[RunOut]) #validates output against RunOut schema
async def fetch_results(
    limit: int = Query(5, ge=1, le=50),
    user = Depends(verify_firebase_token)
):
    return get_recent_runs(limit, user["user_id"])

#route to delete query from database. currently broken and I suspect the front end is the issue
@router.delete("/delete/{entry_id}")
async def delete_record(
    entry_id: str,
    user = Depends(verify_firebase_token) #verify user 
    ):

    #this logic should be moved to the schema dependencies
    try: 
        result = delete_entry(entry_id, user['user_id']) #delete specific entry matching user id and entry id
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"message": "Entry deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#this stays at the end otherwise routes will not be included
app.include_router(router)