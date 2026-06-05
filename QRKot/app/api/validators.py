from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден!",
        )
    return charity_project


async def check_charity_project_full_amount_ge_invested(
    project_full_amount: int,
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project: CharityProject = await charity_project_crud.get(
        project_id,
        session,
    )
    if project_full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    elif project_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Требуемая сумма меньше чем уже собранная сумма!",
        )
    return


async def check_charity_project_not_closed(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project: CharityProject = await charity_project_crud.get(
        project_id,
        session,
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя вносить изменения в уже закрытый проект!",
        )


async def check_charity_project_not_invested(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project: CharityProject = await charity_project_crud.get(
        project_id,
        session,
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нелзя вносить изменения в уже инвестированный проект!",
        )
