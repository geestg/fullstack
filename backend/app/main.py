from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, users, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
