from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User
from app.services.investments import distribute_donations


class CRUDDonation(CRUDBase):
    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()

    async def distribute_funds(
        self,
        actual_donation,
        session: AsyncSession,
    ) -> Optional[Donation]:
        actual_project: CharityProject = await session.execute(
            select(CharityProject)
            .where(~CharityProject.fully_invested)
            .order_by(CharityProject.create_date)
            .with_for_update()
        )
        actual_project = actual_project.scalars().first()
        if not actual_project:
            return
        distribute_donations(
            actual_donation,
            actual_project,
        )
        return actual_donation


donation_crud = CRUDDonation(Donation)
