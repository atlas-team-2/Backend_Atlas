from contextlib import asynccontextmanager

from fastapi import FastAPI

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


@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}


app.include_router(auth.router, prefix='/api/v1')
app.include_router(user.router, prefix='/api/v1')
app.include_router(role.router, prefix='/api/v1')
app.include_router(permission.router, prefix='/api/v1')
app.include_router(nation.router, prefix='/api/v1')
app.include_router(nation_info.router, prefix='/api/v1')
app.include_router(settlement_zone.router, prefix='/api/v1')
app.include_router(costume.router, prefix='/api/v1')
app.include_router(comment.router, prefix='/api/v1')
app.include_router(game.router, prefix='/api/v1')
app.include_router(game_question.router, prefix='/api/v1')
app.include_router(game_option.router, prefix='/api/v1')
