from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_full_amount_ge_invested,
    check_charity_project_not_closed,
    check_charity_project_not_invested,
    check_project_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    description="Показать список всех целевых проектов.",
)
async def get_all_charity_projects(
    session: SessionDep,
):
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    description="Создать целевой проект.",
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    await check_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    return new_charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_not_closed(
        project_id,
        session,
    )
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_charity_project_full_amount_ge_invested(
            obj_in.full_amount,
            project_id,
            session,
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_not_closed(project_id, session)
    await check_charity_project_not_invested(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
