from pydantic import BaseModel, Field
from fastapi import Query
from typing import Annotated
from datetime import datetime, timezone
from db import get_recent_runs_from_db, save_pipeline_run_to_db, delete_entry_from_db


"""
This is the database abstraction layer. pydantic schemas and their dependancies here can be changed,
without altering functions in the db layer, allowing changes to the data saved or 
recalled without refactoring db functions, for more resiliance to future changes
"""


#pydantic model for query parameters
class AnalyzeQueryParams(BaseModel):
    query : str 
    limit : int 
    
#dependency function to extract query parameters via pydantic model
def get_analyze_params(
        query: Annotated[str, Query(description="Research topic to analyze")] = ...,
        limit: Annotated[int, Query(ge=1, le=50, description="Number of papers to return (1-50)")] = 5,
) -> AnalyzeQueryParams:
    return AnalyzeQueryParams(query=query, limit=limit)

#pydantic model for run saving/history
class RunOut(BaseModel):
    id: str #exposed string version of MongoDB objectId
    user_id: str
    query: str
    papers: list
    clusters: dict
    follow_up_hypothesis: dict
    timestamp : datetime

#dependency function to return run history
def get_recent_runs(limit: int, user_id: str) -> list[RunOut]:
    runs = get_recent_runs_from_db(limit, user_id)

    return [
        RunOut(
            id=str(run['_id']),
            user_id=run.get('user_id'),
            query=run.get('query'),
            papers = run.get('papers'),
            clusters = run.get('clusters'),
            follow_up_hypothesis = run.get('follow_up_hypothesis'),
            timestamp=run.get('timestamp')
        )
        for run in runs
    ]

#model to save a run in the database
class RunIn(BaseModel):
    user_id: str
    query: str
    papers: list
    clusters: dict
    follow_up_hypothesis: dict
    timestamp: datetime

#dependency function to save run results
def save_pipeline_run(data: dict) -> RunIn:
    data_to_save = data.copy()
    data_to_save['timestamp'] = datetime.now(timezone.utc) 

    run = RunIn(
       user_id=data_to_save.get('user_id'),
       query=data_to_save.get('query'),
        papers = data_to_save.get('papers'),
        clusters = data_to_save.get('clusters'),
        follow_up_hypothesis = data_to_save.get('follow_up_hypothesis'),
        timestamp=data_to_save.get('timestamp')
    )  

    return save_pipeline_run_to_db(run)

#model to delete entry in database based on object id
class DeleteRun(BaseModel):
    id: str
    user_id: str

#dependency function to delete entry

def delete_entry(id: str, user_id: str):
    delete_run = DeleteRun(
        id=id, 
        user_id=user_id
        )
    return delete_entry_from_db(delete_run)


    