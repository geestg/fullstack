import sys
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from passlib.context import CryptContext

# -----------------------------
# Tambahkan folder backend ke sys.path
# -----------------------------
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, "backend")
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.database import SessionLocal, engine, Base
from app.models import User

# -----------------------------
# Setup hashing password
# -----------------------------
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# -----------------------------
# Pastikan tabel sudah dibuat
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Data users yang ingin dibuat
# -----------------------------
users_to_create = [
    {"username": "admin", "password": "admin123", "full_name": "Administrator"},
    {"username": "budi", "password": "budi123", "full_name": "Budi Santoso"},
    {"username": "siti", "password": "siti123", "full_name": "Siti Aminah"},
]

# -----------------------------
# Cek kolom yang tersedia di tabel User
# -----------------------------
inspector = inspect(engine)
columns = [c['name'] for c in inspector.get_columns('users')]

# -----------------------------
# Buat user baru
# -----------------------------
db = SessionLocal()
try:
    for u in users_to_create:
        hashed_password = pwd_context.hash(u["password"])

        # Hanya masukkan field yang tersedia di tabel
        user_data = {"username": u["username"], "hashed_password": hashed_password}
        if "full_name" in columns:
            user_data["full_name"] = u["full_name"]

        # Cek apakah user sudah ada
        user = db.query(User).filter(User.username == u["username"]).first()
        if user:
            user.hashed_password = hashed_password
            if "full_name" in columns:
                user.full_name = u["full_name"]
            db.commit()
            print(f"[~] User '{u['username']}' sudah ada, info diperbarui!")
        else:
            user = User(**user_data)
            db.add(user)
            db.commit()
            print(f"[+] User '{u['username']}' berhasil dibuat!")
finally:
    db.close()
    print("✅ Selesai membuat semua user.")
