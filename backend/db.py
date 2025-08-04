from pymongo import MongoClient
import os
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME") 
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD") 


client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@ra-agents.yjgi3kb.mongodb.net/?retryWrites=true&w=majority&appName=ra-agents")
collection = client['ra-agents']['pipeline_runs']

def save_pipeline_run_to_db(run):
    """
    save previous run to mongo db
    """
    collection.insert_one(run.model_dump())

def get_recent_runs_from_db(limit, user_id):
    """
    Load previous runs per user id
    """
    runs = list(collection.find({'user_id':user_id})
                .sort('timestamp', -1)
                .limit(limit))
    return runs

def delete_entry_from_db(delete_run):
    to_remove = {
        "_id": ObjectId(delete_run.id),
        "user_id" : delete_run.user_id
        }
    result = collection.delete_one(to_remove)
    return result