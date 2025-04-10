from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from app.database import init_db
from app.api import routes, auth
from app.graphql.schema import schema

from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.utils.rate_limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(routes.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")