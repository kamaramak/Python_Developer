from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from app.services.investments import distribute_donations


class CRUDCharityProject(CRUDBase):
    async def distribute_funds(
        self,
        actual_project,
        session: AsyncSession,
    ):
        actual_donation: Donation = await session.execute(
            select(Donation)
            .where(~Donation.fully_invested)
            .order_by(Donation.create_date)
            .with_for_update()
        )
        actual_donation = actual_donation.scalars().first()
        if not actual_donation:
            return
        distribute_donations(
            actual_donation,
            actual_project,
        )
        return actual_project

    @staticmethod
    async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
