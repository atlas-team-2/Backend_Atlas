from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import NationInfoServiceDep
from app.models.entities.nation_info import (
    NationInfoCreate,
    NationInfoPublic,
    NationInfoUpdate,
)
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/nation-infos',
    tags=['nation-infos'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['nation_info:read'])], responses=auth_responses)
async def get_nation_infos(
    service: NationInfoServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[NationInfoPublic]:
    return await service.get_nation_infos(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['nation_info:create'])], responses=auth_responses)
async def create_nation_info(
    nation_info_create: NationInfoCreate,
    service: NationInfoServiceDep,
) -> NationInfoPublic:
    return await service.create_nation_info(nation_info_create)


@router.get('/{info_id}', dependencies=[require_scopes(['nation_info:read'])], responses={**auth_responses, **detail_responses})
async def get_nation_info(
    info_id: UUID,
    service: NationInfoServiceDep,
) -> NationInfoPublic:
    result = await service.get_nation_info(info_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{info_id}', dependencies=[require_scopes(['nation_info:update'])], responses={**auth_responses, **detail_responses})
async def update_nation_info(
    info_id: UUID,
    nation_info_update: NationInfoUpdate,
    service: NationInfoServiceDep,
) -> NationInfoPublic:
    result = await service.update_nation_info(info_id, nation_info_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{info_id}', dependencies=[require_scopes(['nation_info:delete'])], responses={**auth_responses, **detail_responses})
async def delete_nation_info(
    info_id: UUID,
    service: NationInfoServiceDep,
) -> NationInfoPublic:
    result = await service.delete_nation_info(info_id)
    if result is None:
        raise NotFoundError()
    return result