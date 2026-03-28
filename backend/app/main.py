from fastapi import FastAPI
from .api import articles, comments

app = FastAPI(title="Blog Platform API")

app.include_router(articles.router)
app.include_router(comments.router)