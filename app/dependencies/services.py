from typing import Annotated
from fastapi import Depends

from app.dependencies.repositories import UserRepositoryDep
from app.services.user import UserService
from app.dependencies.repositories import RoleRepositoryDep
from app.services.role import RoleService
from app.dependencies.repositories import PermissionRepositoryDep
from app.services.permission import PermissionService
from app.dependencies.repositories import NationRepositoryDep
from app.services.nation import NationService
from app.dependencies.repositories import CommentRepositoryDep
from app.services.comment import CommentService
from app.services.game import GameService
from app.dependencies.repositories import GameRepositoryDep
from app.dependencies.repositories import GameQuestionRepositoryDep
from app.services.game_question import GameQuestionService
from app.dependencies.repositories import GameOptionRepositoryDep
from app.services.game_option import GameOptionService
from app.dependencies.repositories import CostumeRepositoryDep
from app.services.costume import CostumeService
from app.dependencies.repositories import SettlementZoneRepositoryDep
from app.services.settlement_zone import SettlementZoneService
from app.dependencies.repositories import NationInfoRepositoryDep
from app.services.nation_info import NationInfoService

async def get_user_service(repo: UserRepositoryDep):
    yield UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

async def get_role_service(repo: RoleRepositoryDep):
    yield RoleService(repo)

RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]

async def get_permission_service(repo: PermissionRepositoryDep):
    yield PermissionService(repo)

PermissionServiceDep = Annotated[PermissionService, Depends(get_permission_service)]

async def get_nation_service(repo: NationRepositoryDep):
    yield NationService(repo)

NationServiceDep = Annotated[NationService, Depends(get_nation_service)]

async def get_comment_service(repo: CommentRepositoryDep):
    yield CommentService(repo)

CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]

async def get_game_service(repo: GameRepositoryDep):
    yield GameService(repo)

GameServiceDep = Annotated[GameService, Depends(get_game_service)]

async def get_game_question_service(repo: GameQuestionRepositoryDep):
    yield GameQuestionService(repo)

GameQuestionServiceDep = Annotated[GameQuestionService, Depends(get_game_question_service)]

async def get_game_option_service(repo: GameOptionRepositoryDep):
    yield GameOptionService(repo)

GameOptionServiceDep = Annotated[GameOptionService, Depends(get_game_option_service)]

async def get_costume_service(repo: CostumeRepositoryDep):
    yield CostumeService(repo)

CostumeServiceDep = Annotated[CostumeService, Depends(get_costume_service)]

async def get_settlement_zone_service(repo: SettlementZoneRepositoryDep):
    yield SettlementZoneService(repo)

SettlementZoneServiceDep = Annotated[SettlementZoneService, Depends(get_settlement_zone_service)]

async def get_nation_info_service(repo: NationInfoRepositoryDep):
    yield NationInfoService(repo)

NationInfoServiceDep = Annotated[NationInfoService, Depends(get_nation_info_service)]
