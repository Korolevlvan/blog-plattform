from fastapi import FastAPI

from src.routers import articles, comments, health

app = FastAPI(title="Backend API", version="3.0.0")

app.include_router(health.router)
app.include_router(articles.router, prefix="/api", tags=["posts"])
app.include_router(comments.router, prefix="/api", tags=["comments"])
