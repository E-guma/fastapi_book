from contextlib import asynccontextmanager

from config import SESSION_HTTPS_ONLY, SESSION_SECRET
from data.db import init_db
from fastapi import FastAPI
from set_admin import set_admin
from starlette.middleware.sessions import SessionMiddleware
from web import auth, creature, explorer, google, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables and the admin account."""
    init_db()
    set_admin()
    yield


app = FastAPI(
    title="Cryptid API",
    description="A small API for cataloguing cryptids and the explorers who chase them.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    https_only=SESSION_HTTPS_ONLY,
    same_site="lax",
    max_age=600
)

@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(google.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
