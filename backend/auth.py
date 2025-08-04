import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os
import json

import logging 

"""DONT FORGET TO REVOKE FLY API TOKEN BEFORE DEPLOYING THESE CHANGES
because we are adding redis support, we will need to user docker compose to deploy multiple containers
should probably use kubernetes for this. 
"""
load_dotenv()

#establish connection to firebase and initialize app
#I have minized the firebase credentials and saved in .env instead of saving it as a .json for security
service_account_info = json.loads(os.environ.get("FIREBASE_CREDENTIAL"))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

#verify header token
async def verify_firebase_token(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=401, detail='Missing token')
    
    try:
        id_token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logging.exception("Token verification failed")
        raise HTTPException(status_code=401, detail="Invalid token")
    
#identifier for redis rate limiting
async def user_id_rate_limit_key(request: Request) -> str:
    try:
        token = request.headers.get("Authorization", "")
        if token.startswith("Bearer "):
            id_token = token.split("Bearer ")[1]
            decoded_token = auth.verify_id_token(id_token)
            return f"user: {decoded_token['user_id']}"
    except Exception:
        pass
    return request.client.host #fallback ip address