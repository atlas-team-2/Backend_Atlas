from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.services import GameQuestionServiceDep
from app.models.entities.game_question import (
    GameQuestionCreate,
    GameQuestionPublic,
    GameQuestionUpdate,
)
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/game-questions',
    tags=['game-questions'],
)


@router.get('/')
async def get_game_questions(
    service: GameQuestionServiceDep,
    filters: Annotated[CommonListFilters, Depends()],
) -> Sequence[GameQuestionPublic]:
    return await service.get_game_questions(offset=filters.offset, limit=filters.limit)


@router.post('/')
async def create_game_question(
    game_question_create: GameQuestionCreate,
    service: GameQuestionServiceDep,
) -> GameQuestionPublic:
    return await service.create_game_question(game_question_create)


@router.get('/{game_question_id}')
async def get_game_question(
    game_question_id: UUID,
    service: GameQuestionServiceDep,
) -> Optional[GameQuestionPublic]:
    return await service.get_game_question(game_question_id)


@router.put('/{game_question_id}')
async def update_game_question(
    game_question_id: UUID,
    game_question_update: GameQuestionUpdate,
    service: GameQuestionServiceDep,
) -> Optional[GameQuestionPublic]:
    return await service.update_game_question(game_question_id, game_question_update)


@router.delete('/{game_question_id}')
async def delete_game_question(
    game_question_id: UUID,
    service: GameQuestionServiceDep,
) -> Optional[GameQuestionPublic]:
    return await service.delete_game_question(game_question_id)
