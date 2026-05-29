from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import GameQuestionServiceDep
from app.models.entities.game_question import (
    GameQuestionCreate,
    GameQuestionPublic,
    GameQuestionUpdate,
)
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/game-questions',
    tags=['game-questions'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['game_question:read'])], responses=auth_responses)
async def get_game_questions(
    service: GameQuestionServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[GameQuestionPublic]:
    return await service.get_game_questions(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['game_question:create'])], responses=auth_responses)
async def create_game_question(
    game_question_create: GameQuestionCreate,
    service: GameQuestionServiceDep,
) -> GameQuestionPublic:
    return await service.create_game_question(game_question_create)


@router.get(
    '/{game_question_id}',
    dependencies=[require_scopes(['game_question:read'])],
    responses={**auth_responses, **detail_responses},
)
async def get_game_question(
    game_question_id: UUID,
    service: GameQuestionServiceDep,
) -> GameQuestionPublic:
    result = await service.get_game_question(game_question_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put(
    '/{game_question_id}',
    dependencies=[require_scopes(['game_question:update'])],
    responses={**auth_responses, **detail_responses},
)
async def update_game_question(
    game_question_id: UUID,
    game_question_update: GameQuestionUpdate,
    service: GameQuestionServiceDep,
) -> GameQuestionPublic:
    result = await service.update_game_question(game_question_id, game_question_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete(
    '/{game_question_id}',
    dependencies=[require_scopes(['game_question:delete'])],
    responses={**auth_responses, **detail_responses},
)
async def delete_game_question(
    game_question_id: UUID,
    service: GameQuestionServiceDep,
) -> GameQuestionPublic:
    result = await service.delete_game_question(game_question_id)
    if result is None:
        raise NotFoundError()
    return result