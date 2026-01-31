# backend/setup_db.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ----- DATABASE CONFIG -----
DATABASE_URL = "sqlite:///./test.db"  # ganti sesuai database-mu, contoh: postgresql://user:pass@localhost/dbname
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ----- MODEL -----
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String, nullable=True)  # tambahkan kolom ini

# ----- RESET DATABASE -----
print("Reset database...")
Base.metadata.drop_all(bind=engine)      # HATI-HATI: hapus semua tabel lama
Base.metadata.create_all(bind=engine)    # buat tabel baru
print("Database reset selesai.")

# ----- TAMBAH USER CONTOH -----
db = SessionLocal()
new_user = User(username="glen", password="1234", full_name="Glen")
db.add(new_user)
db.commit()
db.refresh(new_user)

print("User baru berhasil ditambahkan:")
print(f"ID: {new_user.id}, Username: {new_user.username}, Full Name: {new_user.full_name}")
db.close()
