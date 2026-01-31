from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
