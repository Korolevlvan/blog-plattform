from fastapi import FastAPI
from src.routes.user_routes import router as user_router
from src.routes.article_routes import router as article_router
from src.routes.comment_routes import router as comment_router
from src.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Platform API")

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(article_router, prefix="/api", tags=["Articles"])
app.include_router(comment_router, prefix="/api", tags=["Comments"])