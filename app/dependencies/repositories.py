from typing import Annotated

from fastapi import Depends

from app.repositories.comment import CommentRepository
from app.repositories.costume import CostumeRepository
from app.repositories.game import GameRepository
from app.repositories.game_option import GameOptionRepository
from app.repositories.game_question import GameQuestionRepository
from app.repositories.nation import NationRepository
from app.repositories.nation_info import NationInfoRepository
from app.repositories.permission import PermissionRepository
from app.repositories.refresh_session import RefreshSessionRepository
from app.repositories.role import RoleRepository
from app.repositories.settlement_zone import SettlementZoneRepository
from app.repositories.user import UserRepository

UserRepositoryDep = Annotated[
    UserRepository,
    Depends(UserRepository),
]
RoleRepositoryDep = Annotated[
    RoleRepository,
    Depends(RoleRepository),
]
PermissionRepositoryDep = Annotated[
    PermissionRepository,
    Depends(PermissionRepository),
]
NationRepositoryDep = Annotated[
    NationRepository,
    Depends(NationRepository),
]
CommentRepositoryDep = Annotated[
    CommentRepository,
    Depends(CommentRepository),
]
GameRepositoryDep = Annotated[
    GameRepository,
    Depends(GameRepository),
]
GameQuestionRepositoryDep = Annotated[
    GameQuestionRepository,
    Depends(GameQuestionRepository),
]
GameOptionRepositoryDep = Annotated[
    GameOptionRepository,
    Depends(GameOptionRepository),
]
CostumeRepositoryDep = Annotated[
    CostumeRepository,
    Depends(CostumeRepository),
]
SettlementZoneRepositoryDep = Annotated[
    SettlementZoneRepository,
    Depends(SettlementZoneRepository),
]
NationInfoRepositoryDep = Annotated[
    NationInfoRepository,
    Depends(NationInfoRepository),
]
RefreshSessionRepositoryDep = Annotated[
    RefreshSessionRepository,
    Depends(RefreshSessionRepository),
]
