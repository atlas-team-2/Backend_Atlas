from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import GameOptionServiceDep
from app.models.entities.game_option import GameOptionCreate, GameOptionUpdate, GameOptionPublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/game-options",
    tags=["game-options"],
)

@router.get("/")
async def get_game_options(
    service: GameOptionServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[GameOptionPublic]:
    return await service.get_game_options(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_game_option(
    game_option_create: GameOptionCreate,
    service: GameOptionServiceDep,
) -> GameOptionPublic:
    return await service.create_game_option(game_option_create)

@router.get("/{game_option_id}")
async def get_game_option(
    game_option_id: UUID,
    service: GameOptionServiceDep,
) -> Optional[GameOptionPublic]:
    return await service.get_game_option(game_option_id)

@router.put("/{game_option_id}")
async def update_game_option(
    game_option_id: UUID,
    game_option_update: GameOptionUpdate,
    service: GameOptionServiceDep,
) -> Optional[GameOptionPublic]:
    return await service.update_game_option(game_option_id, game_option_update)

@router.delete("/{game_option_id}")
async def delete_game_option(
    game_option_id: UUID,
    service: GameOptionServiceDep,
) -> Optional[GameOptionPublic]:
    return await service.delete_game_option(game_option_id)
