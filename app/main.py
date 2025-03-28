from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.api import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)