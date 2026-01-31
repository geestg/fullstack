# backend/setup_db_postgres.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ----- DATABASE CONFIG POSTGRESQL -----
# Ganti sesuai konfigurasi Postgres-mu
DB_USER = "postgres"
DB_PASSWORD = "1"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "fullstack_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ----- MODEL USER -----
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String, nullable=True)

# ----- RESET DATABASE -----
print("Reset database PostgreSQL...")
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
