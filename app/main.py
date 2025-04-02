from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from app.database import init_db
from app.api import routes
from app.graphql.schema import schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")