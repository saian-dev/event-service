from typing import Annotated
from fastapi import Depends

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models.event import EventCategory, Event


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_categories(self, limit: int | None = None, offset: int | None = None):
        qs = select(EventCategory)
        if limit is not None and offset is not None:
            qs = qs.limit(limit).offset(offset)
        return (await self.db.execute(qs)).scalars().all()

    async def create_category(self, **kwargs: dict):
        qs = insert(EventCategory).values(**kwargs).returning(EventCategory.name)
        qs = await self.db.execute(qs)

        await self.db.commit()
        return qs.mappings().one()

    async def get_events(self, limit: int | None = None, offset: int | None = None):
        qs = select(Event)
        if limit is not None and offset is not None:
            qs = qs.limit(limit).offset(offset)
        return (await self.db.execute(qs)).scalars().all()


async def get_event_service(db: Annotated[AsyncSession, Depends(get_db_session)]) -> EventService:
    return EventService(db=db)
