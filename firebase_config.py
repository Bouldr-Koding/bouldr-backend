import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

cred_path = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
