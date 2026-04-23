from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import GameServiceDep
from app.models.entities.game import GameCreate, GameUpdate, GamePublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/games",
    tags=["games"],
)

@router.get("/")
async def get_games(
    service: GameServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[GamePublic]:
    return await service.get_games(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_game(
    game_create: GameCreate,
    service: GameServiceDep,
) -> GamePublic:
    return await service.create_game(game_create)

@router.get("/{game_id}")
async def get_game(
    game_id: UUID,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.get_game(game_id)

@router.put("/{game_id}")
async def update_game(
    game_id: UUID,
    game_update: GameUpdate,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.update_game(game_id, game_update)

@router.delete("/{game_id}")
async def delete_game(
    game_id: UUID,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.delete_game(game_id)
