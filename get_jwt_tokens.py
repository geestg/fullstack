# create_users.py / get_jwt_tokens.py
from sqlalchemy.orm import Session
from app.models import User
from app.database import SessionLocal, engine
from passlib.context import CryptContext
import requests
import os

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# File untuk menyimpan token
jwt_file = "jwt_tokens.txt"

# API endpoint login
api_url = "http://127.0.0.1:8000/auth/login"

# User yang ingin dibuat
users_to_create = [
    {"username": "admin", "password": "admin123", "full_name": "Admin"},
    {"username": "budi", "password": "budi123", "full_name": "Budi"},
    {"username": "siti", "password": "siti123", "full_name": "Siti"}
]

# Buat session database
db: Session = SessionLocal()

for u in users_to_create:
    # Hash password
    hashed = pwd_context.hash(u["password"])

    # Cek user sudah ada atau belum
    existing_user = db.query(User).filter(User.username == u["username"]).first()
    if existing_user:
        print(f"[SKIP] User {u['username']} sudah ada")
        continue

    # Buat user baru
    user = User(
        username=u["username"],
        password=hashed,   # <--- ganti dari hashed_password ke password
        full_name=u["full_name"]
    )
    db.add(user)
db.commit()
db.close()

print("[✅] Semua user berhasil dibuat di database.")

# Generate JWT token untuk masing-masing user
with open(jwt_file, "w") as f:
    for u in users_to_create:
        try:
            r = requests.post(api_url, data={"username": u["username"], "password": u["password"]})
            if r.status_code == 200:
                token = r.json().get("access_token")
                f.write(f"{u['username']}: {token}\n")
                print(f"[+] JWT token untuk {u['username']} berhasil dibuat!")
            else:
                print(f"[FAILED] {u['username']} -> {r.status_code} {r.text}")
        except Exception as e:
            print(f"[ERROR] {u['username']} -> {e}")

print(f"[✅] Semua token disimpan di {jwt_file}")
