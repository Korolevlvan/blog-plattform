from fastapi import FastAPI
from app.api.routes import health, users

app = FastAPI(title="users-api", version="2.0.0", docs_url="/users-docs", openapi_url="/users-openapi.json")

app.include_router(health.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {
        "service": "users-api",
        "docs": "/docs",
        "message": "Users and auth service",
    }
