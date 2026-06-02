from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.error_handler import exception_handler
from app.core.middlewares import request_logging_middleware
from app.core.responses import common_responses
from app.core.settings import settings
from app.routers import (
    auth,
    comment,
    costume,
    game,
    game_option,
    game_question,
    health,
    nation,
    nation_info,
    permission,
    role,
    settlement_zone,
    user,
)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit.default_limit],
)

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    servers=settings.app.servers,
    docs_url=None,
    openapi_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
    max_age=settings.cors.max_age,
)

app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=exception_handler,
)

app_router = APIRouter(
    prefix='/api/v1',
    responses=common_responses,
)

app_router.include_router(health.router)
app_router.include_router(auth.router)
app_router.include_router(user.router)
app_router.include_router(role.router)
app_router.include_router(permission.router)
app_router.include_router(nation.router)
app_router.include_router(nation_info.router)
app_router.include_router(settlement_zone.router)
app_router.include_router(costume.router)
app_router.include_router(comment.router)
app_router.include_router(game.router)
app_router.include_router(game_question.router)
app_router.include_router(game_option.router)

app.include_router(app_router)
app.middleware('http')(request_logging_middleware)


@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}
