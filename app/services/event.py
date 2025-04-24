from typing import Annotated, Type
from fastapi import Depends

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import joinedload, Query
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session, Base
from app.models.event import EventCategory, Event


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def __filter_qs(model: Type[Base], qs: Query | Select, filters: dict) -> Query:
        orm_operators_mapping = {
            "eq": lambda v: ("__eq__", filter_value),
            "ilike": lambda v: ("ilike", filter_value),
        }

        for field_filter_name, filter_value in filters.items():
            # todo: support more operators: gre, lte, gr, lt etc
            # check this library for inspiration https://github.com/arthurio/fastapi-filter/blob/main/fastapi_filter/contrib/sqlalchemy/filter.py#L33
            if "__" in field_filter_name:
                name, operator = field_filter_name.split("__")
            else:
                name, operator = field_filter_name, "eq"
            operator, value = orm_operators_mapping[operator](filter_value)
            field = getattr(model, name)
            qs = qs.filter(getattr(field, operator)(value))
        return qs

    async def get_categories(self, limit: int | None = None, offset: int | None = None, **filters):
        qs = select(EventCategory)
        if limit is not None and offset is not None:
            qs = qs.limit(limit).offset(offset)

        if filters:
            qs = self.__filter_qs(EventCategory, qs, filters)

        return (await self.db.execute(qs)).scalars().all()

    async def create_category(self, **kwargs: dict):
        qs = insert(EventCategory).values(**kwargs).returning(EventCategory.name)
        qs = await self.db.execute(qs)

        await self.db.commit()
        return qs.mappings().one()

    async def delete_category(self, name: str) -> bool:
        qs = delete(EventCategory).where(EventCategory.name == name)
        res = await self.db.execute(qs)
        await self.db.commit()
        return res.rowcount != 0

    async def get_events(self, limit: int | None = None, offset: int | None = None, **filters):
        qs = select(Event).options(joinedload(Event.category))
        if limit is not None and offset is not None:
            qs = qs.limit(limit).offset(offset)

        if filters:
            qs = self.__filter_qs(Event, qs, filters)

        return (await self.db.execute(qs)).scalars().all()

    async def get_event(self, event_id: int):
        qs = select(Event).where(Event.id == event_id).options(joinedload(Event.category))
        event = (await self.db.execute(qs)).scalars().first()
        return event

    async def delete_event(self, event_id: int) -> bool:
        qs = delete(Event).where(Event.id == event_id)
        res = await self.db.execute(qs)
        await self.db.commit()
        return res.rowcount != 0


async def get_event_service(db: Annotated[AsyncSession, Depends(get_db_session)]) -> EventService:
    return EventService(db=db)
