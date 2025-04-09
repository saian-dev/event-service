from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.services.event import EventService


router = APIRouter()


class EventCategorySchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


@router.get("/", response_model=list[EventCategorySchema])
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db_session)]):
    server = EventService(db=db)
    categories = await server.get_all_categories()
    return categories
