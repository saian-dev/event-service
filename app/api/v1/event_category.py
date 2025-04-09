from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models import EventCategory as EventCategoryModel


router = APIRouter()


class EventCategorySchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


@router.get("/", response_model=EventCategorySchema)
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db_session)]):
    categories = await EventCategoryModel.get_all(db)
    return categories
