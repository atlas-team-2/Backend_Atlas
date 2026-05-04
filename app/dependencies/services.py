from typing import Annotated

from fastapi import Depends

from app.services.comment import CommentService
from app.services.costume import CostumeService
from app.services.game import GameService
from app.services.game_option import GameOptionService
from app.services.game_question import GameQuestionService
from app.services.nation import NationService
from app.services.nation_info import NationInfoService
from app.services.permission import PermissionService
from app.services.refresh import RefreshSessionService
from app.services.role import RoleService
from app.services.settlement_zone import SettlementZoneService
from app.services.user import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
RoleServiceDep = Annotated[RoleService, Depends(RoleService)]
PermissionServiceDep = Annotated[PermissionService, Depends(PermissionService)]
NationServiceDep = Annotated[NationService, Depends(NationService)]
CommentServiceDep = Annotated[CommentService, Depends(CommentService)]
GameServiceDep = Annotated[GameService, Depends(GameService)]
GameQuestionServiceDep = Annotated[GameQuestionService, Depends(GameQuestionService)]
GameOptionServiceDep = Annotated[GameOptionService, Depends(GameOptionService)]
CostumeServiceDep = Annotated[CostumeService, Depends(CostumeService)]
SettlementZoneServiceDep = Annotated[
    SettlementZoneService, Depends(SettlementZoneService)
]
NationInfoServiceDep = Annotated[NationInfoService, Depends(NationInfoService)]
RefreshSessionServiceDep = Annotated[
    RefreshSessionService,
    Depends(RefreshSessionService),
]
