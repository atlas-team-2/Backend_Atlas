from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import GameOptionServiceDep
from app.models.entities.game_option import (
    GameOptionCreate,
    GameOptionPublic,
    GameOptionUpdate,
)
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/game-options',
    tags=['game-options'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['game_option:read'])], responses=auth_responses)
async def get_game_options(
    service: GameOptionServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[GameOptionPublic]:
    return await service.get_game_options(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['game_option:create'])], responses=auth_responses)
async def create_game_option(
    game_option_create: GameOptionCreate,
    service: GameOptionServiceDep,
) -> GameOptionPublic:
    return await service.create_game_option(game_option_create)


@router.get('/{game_option_id}', dependencies=[require_scopes(['game_option:read'])], responses={**auth_responses, **detail_responses})
async def get_game_option(
    game_option_id: UUID,
    service: GameOptionServiceDep,
) -> GameOptionPublic:
    result = await service.get_game_option(game_option_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{game_option_id}', dependencies=[require_scopes(['game_option:update'])], responses={**auth_responses, **detail_responses})
async def update_game_option(
    game_option_id: UUID,
    game_option_update: GameOptionUpdate,
    service: GameOptionServiceDep,
) -> GameOptionPublic:
    result = await service.update_game_option(game_option_id, game_option_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete(
    '/{game_option_id}',
    dependencies=[require_scopes(['game_option:delete'])],
    responses={**auth_responses, **detail_responses},
)
async def delete_game_option(
    game_option_id: UUID,
    service: GameOptionServiceDep,
) -> GameOptionPublic:
    result = await service.delete_game_option(game_option_id)
    if result is None:
        raise NotFoundError()
    return result