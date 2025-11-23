from fastapi import FastAPI, HTTPException, Response

from typing import Optional
import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
from pydantic import BaseModel, Field

app = FastAPI() # Create FastAPI instance
# ---------------------------
# FIREBASE INITIALIZATION
# ---------------------------

cred_path = "serviceAccountKey.json"
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------------------
# BaseModels
# ---------------------------

class UserStats(BaseModel):
    hardestGrade: str
    totalPoints: int
    totalSends: int

class UserDetails(BaseModel):
    createdAt: datetime = Field(..., description="Date time string")
    displayName: Optional[str] = None
    email: Optional[str] = None
    stats: UserStats


# ---------------------------
# API'S 
# ---------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to backend"}


@app.post("/users/registration/create/{userId}")
def user_reg_create_acc(user_id: str, user_details: UserDetails):
    try:
        user_data = user_details.model_dump()
        doc = db.collection("users").document(user_id)
        doc.set(user_data)
        return Response(status_code=200, content="Successfully registered user:{user_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/database/insert")
# def db_ins():
#     return {"message": "Welcome to db/insert"}

# @app.get("/user/update/sends")
# def get_items():
#     return {"message": "Welcome to db/insert"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)