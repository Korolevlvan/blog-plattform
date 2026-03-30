from fastapi import FastAPI

from src.routes import users, articles, comments

app = FastAPI(
    title="Blog Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)
