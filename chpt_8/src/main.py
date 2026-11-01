from contextlib import asynccontextmanager
from fastapi import FastAPI
from web import creature, explorer
from data.init import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise database tables"""
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(explorer.router)
app.include_router(creature.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
