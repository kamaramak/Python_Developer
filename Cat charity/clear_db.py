from sqlalchemy import delete

from app.core.db import AsyncSessionLocal
from app.models import CharityProject, Donation, User


async def clear_database():
    async with AsyncSessionLocal() as session:
        await session.execute(delete(CharityProject))
        await session.execute(delete(Donation))
        await session.execute(delete(User))
        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(clear_database())
