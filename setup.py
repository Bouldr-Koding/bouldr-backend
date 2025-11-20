# setup_firestore.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ---------------------------
# FIREBASE INITIALIZATION
# ---------------------------

cred_path = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ==========================================
# 1️⃣ Create a Gym
# ==========================================
def create_gym():
    gym_id = "bhub"

    data = {
        "name": "BHUB Bouldering Gym",
        "slug": "bhub",
        "location": {
            "city": "Kuala Lumpur",
            "country": "MY"
        },
        "walls": [
            {"id": "spray_wall", "name": "Spray Wall", "angle": 45},
            {"id": "main_wall", "name": "Main Wall", "angle": 30}
        ],
        "settings": {
            "gradeSystem": {
                "gradeType": "V",
                "highestGrade": "V10",
                "lowestGrade": "V0"},
        }
    }

    db.collection("gyms").document(gym_id).set(data)
    print("✔ Created gym:", gym_id)

    return gym_id


# ==========================================
# 2️⃣ Create Sample Routes for the Gym
# ==========================================
def create_routes(gym_id):
    routes = [
        {
            "id": "b7_purple_crimps",
            "name": "Purple Crimps of Doom",
            "wallId": "main_wall",
            "grade": "B7",
            "color": "purple",
            "styleTags": ["crimpy", "power"],
            "setter": "Daryl",
            "isActive": True,
            "setDate": datetime.utcnow().isoformat() + "Z",
            "qrCode": "BHUB-B7-001"
        },
        {
            "id": "b5_green_jugs",
            "name": "Green Jug Party",
            "wallId": "spray_wall",
            "grade": "B5",
            "color": "green",
            "styleTags": ["jugs", "fun"],
            "setter": "Zhen",
            "isActive": True,
            "setDate": datetime.utcnow().isoformat() + "Z",
            "qrCode": "BHUB-B5-002"
        }
    ]

    for r in routes:
        db.collection("gyms").document(gym_id) \
            .collection("routes").document(r["id"]).set(r)
        print("✔ Created route:", r["id"])


# ==========================================
# 3️⃣ Create a User
# ==========================================
def create_user():
    user_id = "user_001"

    data = {
        "displayName": "Zhen",
        "email": "zhen@example.com",
        "homeGymId": "bhub",
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "stats": {
            "totalSends": 0,
            "hardestGrade": None,
            "totalPoints": 0
        }
    }

    db.collection("users").document(user_id).set(data)
    print("✔ Created user:", user_id)

    return user_id


# ==========================================
# 4️⃣ Create Sample Climb Logs for User
# ==========================================
def create_user_climbs(user_id):
    climbs = [
        {
            "routeId": "b7_purple_crimps",
            "gymId": "bhub",
            "routeGrade": "B7",
            "routeColor": "purple",
            "tries": 3,
            "style": "send",
            "points": 450,
            "loggedAt": datetime.utcnow().isoformat() + "Z"
        },
        {
            "routeId": "b5_green_jugs",
            "gymId": "bhub",
            "routeGrade": "B5",
            "routeColor": "green",
            "tries": 1,
            "style": "flash",
            "points": 220,
            "loggedAt": datetime.utcnow().isoformat() + "Z"
        }
    ]

    for c in climbs:
        doc_ref = db.collection("users").document(user_id) \
                     .collection("climbs").document()
        doc_ref.set(c)

    print("✔ Added sample climb logs for user", user_id)


# ==========================================
# 5️⃣ Create Leaderboard Collection
# ==========================================
def create_leaderboard():
    leaderboard_id = "bhub_monthly_2025_11"

    data = {
        "scope": "gym_monthly",
        "gymId": "bhub",
        "period": "2025-11",
        "entries": [
            {"userId": "user_001", "displayName": "Zhen", "points": 670},
            {"userId": "user_abc", "displayName": "Moto", "points": 540}
        ],
        "updatedAt": datetime.utcnow().isoformat() + "Z"
    }

    db.collection("leaderboards").document(leaderboard_id).set(data)

    print("✔ Created leaderboard:", leaderboard_id)


# ==========================================
# 6️⃣ Create a Competition Collection
# ==========================================
def create_competition():
    comp_id = "bhub_spraywall_jam_2025"

    data = {
        "gymId": "bhub",
        "name": "BHUB Spray Wall Jam 2025",
        "start": "2025-12-01T10:00:00Z",
        "end": "2025-12-01T22:00:00Z",
        "routes": ["b7_purple_crimps", "b5_green_jugs"],
        "scoring": {
            "type": "points",
            "flashBonus": 10
        }
    }

    db.collection("competitions").document(comp_id).set(data)

    print("✔ Created competition:", comp_id)


# ==========================================
# RUN ALL INITIALIZERS
# ==========================================
if __name__ == "__main__":
    gym_id = create_gym()
    create_routes(gym_id)

    user_id = create_user()
    create_user_climbs(user_id)

    create_leaderboard()
    create_competition()

    print("\n🔥 Firestore setup completed successfully!")
