from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    description="Показать список всех пожертвований.",
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep,
):
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
    description=(
        "Список пожертвований пользователя, выполняющего "
        "запрос.\n\nТолько для зарегистрированных пользователей."
    ),
)
async def get_user_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    return await donation_crud.get_by_user(session, user)


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    description="Создать пожертвование.",
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation
