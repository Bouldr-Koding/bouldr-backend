from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional, List
import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
from pydantic import BaseModel, Field
import json
import re

app = FastAPI() # Create FastAPI instance
load_dotenv()
NEXT_FRONTEND_URL = os.getenv("NEXT_FRONTEND_URL")
# ---------------------------
# CORS (for frontend-backend communication)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", NEXT_FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# FIREBASE INITIALIZATION
# ---------------------------
FIRESTORE_CRED = json.loads(os.environ['FIREBASE'])

if not firebase_admin._apps:
    cred = credentials.Certificate(FIRESTORE_CRED)
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

class Location(BaseModel):
    city: str   # e.g. Use ISO-3166-2 
    country: str  # e.g. Use ISO-3166-2 


class Wall(BaseModel):
    wallId: int
    wallName: str


class Gym(BaseModel):
    gradeSystem: List[str]
    gradingType: str
    name: str
    slug: str
    location: Location
    walls: List[Wall] = Field(default_factory=list)
    
    
# ---------------------------
# Helpers
# ---------------------------

def generate_gym_id(slug: str, location: Location) -> str:
    def norm(part: str) -> str:
        # lowercase and keep only letters/numbers
        return re.sub(r"[^a-z0-9]", "", part.lower())

    slug_part = norm(slug)
    city_part = norm(location.city)
    country_part = norm(location.country)

    return f"{slug_part}-{city_part}-{country_part}"


# ---------------------------
# API'S 
# ---------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to backend"}

@app.post("/users/registration/create/{user_id}")
def user_reg_create_acc(user_id: str, user_details: UserDetails):
    try:
        user_data = user_details.model_dump()
        doc = db.collection("users").document(user_id)
        if doc.get().exists:
            return Response(status_code=200, content=f"User with ID:{user_id} already exists!", )  
        else:      
            doc.set(user_data)
            return Response(status_code=200, content=f"Successfully registered user:{user_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# dont need anymore
# @app.get("/users/registration/exists/{user_id}")
# def user_exists(user_id: str):
#     try:
#         doc = db.collection("users").document(user_id).get()
#         if not doc.exists:
#             raise HTTPException(status_code=404, detail="User not found")
#         return doc.to_dict()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/gyms/registration/create")
def gym_reg_create(gym: Gym):
    try:
        gym_id = generate_gym_id(gym.slug, gym.location)
        doc = db.collection("gyms").document(gym_id)
        if doc.get().exists:
            return Response(status_code=200, content=f"Gym with ID:{gym_id} already exists!")
        gym_data = gym.model_dump()
        doc.set(gym_data)
        return Response(status_code=200, content=f"Successfully registered gym:{gym_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("gyms/registration/exists/{gym_id}")
# def gym_exists(gym_id: str):
#     try:
#         doc = db.collection("gyms").document(gym_id).get()
#         if not doc.exists:
#             raise HTTPException(status_code=404, detail="Gym not found")
#         return doc.to_dict()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/database/insert")
# def db_ins():
#     return {"message": "Welcome to db/insert"}

# @app.get("/user/update/sends")
# def get_items():
#     return {"message": "Welcome to db/insert"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
