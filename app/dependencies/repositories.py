from typing import Annotated
from fastapi import Depends

from app.dependencies.session import SessionDep
from app.repositories.user import UserRepository
from app.repositories.role import RoleRepository
from app.repositories.permission import PermissionRepository
from app.repositories.nation import NationRepository
from app.repositories.comment import CommentRepository
from app.repositories.game import GameRepository
from app.repositories.game_question import GameQuestionRepository
from app.repositories.game_option import GameOptionRepository
from app.repositories.costume import CostumeRepository
from app.repositories.settlement_zone import SettlementZoneRepository
from app.repositories.nation_info import NationInfoRepository

async def get_user_repository(session: SessionDep):
    yield UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

async def get_role_repository(session: SessionDep):
    yield RoleRepository(session)

RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]

async def get_permission_repository(session: SessionDep):
    yield PermissionRepository(session)

PermissionRepositoryDep = Annotated[PermissionRepository, Depends(get_permission_repository)]

async def get_nation_repository(session: SessionDep):
    yield NationRepository(session)

NationRepositoryDep = Annotated[NationRepository, Depends(get_nation_repository)]

async def get_comment_repository(session: SessionDep):
    yield CommentRepository(session)

CommentRepositoryDep = Annotated[CommentRepository, Depends(get_comment_repository)]

async def get_game_repository(session: SessionDep):
    yield GameRepository(session)

GameRepositoryDep = Annotated[GameRepository, Depends(get_game_repository)]


async def get_game_question_repository(session: SessionDep):
    yield GameQuestionRepository(session)

GameQuestionRepositoryDep = Annotated[GameQuestionRepository, Depends(get_game_question_repository)]

async def get_game_option_repository(session: SessionDep):
    yield GameOptionRepository(session)

GameOptionRepositoryDep = Annotated[GameOptionRepository, Depends(get_game_option_repository)]

async def get_costume_repository(session: SessionDep):
    yield CostumeRepository(session)

CostumeRepositoryDep = Annotated[CostumeRepository, Depends(get_costume_repository)]

async def get_settlement_zone_repository(session: SessionDep):
    yield SettlementZoneRepository(session)

SettlementZoneRepositoryDep = Annotated[SettlementZoneRepository, Depends(get_settlement_zone_repository)]

async def get_nation_info_repository(session: SessionDep):
    yield NationInfoRepository(session)

NationInfoRepositoryDep = Annotated[NationInfoRepository, Depends(get_nation_info_repository)]
