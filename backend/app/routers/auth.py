from fastapi import APIRouter, HTTPException
from ..auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login():
    # hardcode user (sesuai instruksi soal)
    token = create_access_token({"sub": "admin"})
    return {"access_token": token, "token_type": "bearer"}
