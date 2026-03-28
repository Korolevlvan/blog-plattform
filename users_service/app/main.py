from fastapi import FastAPI
from .api import users, articles, comments
from .core.database import engine, Base
from app.api.users import router as users_router
from app.api.articles import router as articles_router
from app.api.comments import router as comments_router

# Создаём таблицы (для разработки, в проде лучше миграции)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Platform API")
app.include_router(users_router)

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)