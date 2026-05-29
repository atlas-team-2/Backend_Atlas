from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.core.error_handler import exception_handler
from app.core.middlewares import request_logging_middleware
from app.core.responses import common_responses
from app.core.settings import settings
from app.db.engine import async_session_maker
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.routers import (
    auth,
    comment,
    costume,
    game,
    game_option,
    game_question,
    nation,
    nation_info,
    permission,
    role,
    settlement_zone,
    user,
)
from app.services.bootstrapper import Bootstrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        bootstrapper = Bootstrapper(
            role_repository=RoleRepository(session),
            permission_repository=PermissionRepository(session),
            user_repository=UserRepository(session),
        )
        await bootstrapper.bootstrap()
    yield


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    lifespan=lifespan,
)

app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=exception_handler,
)

app_router = APIRouter(
    prefix='/api/v1',
    responses=common_responses,
)

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