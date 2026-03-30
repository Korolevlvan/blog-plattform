from fastapi import FastAPI
from app.api.routes import articles, comments, health

app = FastAPI(title="backend", version="2.0.0", docs_url="/backend-docs", openapi_url="/backend-openapi.json")

app.include_router(health.router)
app.include_router(articles.router)
app.include_router(comments.router)

@app.get("/")
def root():
    return {
        "service": "backend",
        "docs": "/docs",
        "message": "Posts and comments service",
    }
