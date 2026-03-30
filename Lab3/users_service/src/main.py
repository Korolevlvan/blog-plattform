from fastapi import FastAPI

from src.routers import health, users

app = FastAPI(title="Users API", version="3.0.0")

app.include_router(health.router)
app.include_router(users.router, prefix="/api", tags=["users"])
