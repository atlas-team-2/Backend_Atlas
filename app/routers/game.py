from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_scopes
from app.dependencies.services import GameServiceDep
from app.models.entities.game import GameCreate, GamePublic, GameUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/games',
    tags=['games'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['game:read'])])
async def get_games(
    service: GameServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[GamePublic]:
    return await service.get_games(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['game:create'])])
async def create_game(
    game_create: GameCreate,
    service: GameServiceDep,
) -> GamePublic:
    return await service.create_game(game_create)


@router.get('/{game_id}', dependencies=[require_scopes(['game:read'])])
async def get_game(
    game_id: UUID,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.get_game(game_id)


@router.put('/{game_id}', dependencies=[require_scopes(['game:update'])])
async def update_game(
    game_id: UUID,
    game_update: GameUpdate,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.update_game(game_id, game_update)


@router.delete('/{game_id}', dependencies=[require_scopes(['game:delete'])])
async def delete_game(
    game_id: UUID,
    service: GameServiceDep,
) -> Optional[GamePublic]:
    return await service.delete_game(game_id)
