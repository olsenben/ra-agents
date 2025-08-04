from fastapi import FastAPI, Query, Depends, HTTPException, Header, APIRouter
from backend.agent_ochestration import build_pipeline
from backend.db import save_pipeline_run, get_recent_runs
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME") 
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD") 

print(MONGODB_USERNAME)
print(MONGODB_PASSWORD)

API_URL = "http://localhost:8000"
API_KEY = os.environ.get("FLY_API_TOKEN") 

#load history
history = requests.get(
                f'{API_URL}'+'/results', 
                params={
                    "limit" : 2
                    },
                headers = {
                    "X-API-Key": API_KEY
                    }
                )

history.raise_for_status()
runs = history.json()
options=[f"{run['query']}" for run in runs]
print(options)