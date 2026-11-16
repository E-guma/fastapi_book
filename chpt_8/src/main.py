from contextlib import asynccontextmanager
from fastapi import FastAPI
from web import creature, explorer, auth, user
from data.init import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables."""
    init_db()
    yield


app = FastAPI(
    title="Cryptid API",
    description="A small API for cataloguing cryptids and the explorers who chase them.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(explorer.router)
app.include_router(creature.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
