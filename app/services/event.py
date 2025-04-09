from app.models.event import EventCategory

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self):
        return (await self.db.execute(select(EventCategory))).scalars().all()
