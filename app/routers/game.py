from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import GameServiceDep
from app.models.entities.game import GameCreate, GamePublic, GameUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/games',
    tags=['games'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['game:read'])], responses=auth_responses)
async def get_games(
    service: GameServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[GamePublic]:
    return await service.get_games(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['game:create'])], responses=auth_responses)
async def create_game(
    game_create: GameCreate,
    service: GameServiceDep,
) -> GamePublic:
    return await service.create_game(game_create)


@router.get('/{game_id}', dependencies=[require_scopes(['game:read'])], responses={**auth_responses, **detail_responses})
async def get_game(
    game_id: UUID,
    service: GameServiceDep,
) -> GamePublic:
    result = await service.get_game(game_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{game_id}', dependencies=[require_scopes(['game:update'])], responses={**auth_responses, **detail_responses})
async def update_game(
    game_id: UUID,
    game_update: GameUpdate,
    service: GameServiceDep,
) -> GamePublic:
    result = await service.update_game(game_id, game_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{game_id}', dependencies=[require_scopes(['game:delete'])], responses={**auth_responses, **detail_responses})
async def delete_game(
    game_id: UUID,
    service: GameServiceDep,
) -> GamePublic:
    result = await service.delete_game(game_id)
    if result is None:
        raise NotFoundError()
    return result