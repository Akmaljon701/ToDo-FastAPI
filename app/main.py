from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin

from .auth import auth_router
from .database import Base
from app.utils.redis_service import get_redis, get_cache
from .utils.middlewares import handle_integrity_errors
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.users.routes import user_router
from app.tasks.routes import task_router

# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Load the redis connection
    _app.redis = await get_redis()

    try:
        redis_cache = await get_cache()
        FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
        yield

    finally:
        await _app.redis.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(BaseHTTPMiddleware, dispatch=handle_integrity_errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

routers = [
    auth_router,
    user_router,
    task_router
]

[app.include_router(router) for router in routers]

admin = Admin(app, Base)

