import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine
from app.db import models
from app.api import auth, games, leaderboard, analytics


# load title and version from .env
app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION)

# routes
app.include_router(auth.router)
app.include_router(games.router)
app.include_router(leaderboard.router)
app.include_router(analytics.router)

# create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.get("/")
def read_root():
    return {"message": "Welcome to Time It Right Game API"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
