import http
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from app.services.event import get_event_service, EventService
from .schemas import (
    EventCategoryOutSchema,
    EventOutSchema,
    EventCategoryInSchema,
    EventFilterSchema,
    PaginationSchema,
)

router = APIRouter()


# CATEGORIES
@router.get("/categories", response_model=list[EventCategoryOutSchema])
async def get_all_categories(
    pagination: Annotated[PaginationSchema, Query()],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    categories = await event_service.get_categories(
        limit=pagination.limit, offset=pagination.offset
    )
    return categories


@router.post("/categories", response_model=EventCategoryOutSchema)
async def create_category(
    category: EventCategoryInSchema,
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    try:
        created = await event_service.create_category(**category.dict())
    except IntegrityError:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST, detail="Category already exists"
        )
    else:
        return created


# EVENTS
@router.get("/events", response_model=list[EventOutSchema])
async def get_events(
    filters: Annotated[EventFilterSchema, Query()],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    events = await event_service.get_events(**filters.dict(exclude_unset=True, by_alias=True))
    return events


@router.get("/events/{event_id}", response_model=EventOutSchema)
async def get_event(
    event_id: int, event_service: Annotated[EventService, Depends(get_event_service)]
):
    event = await event_service.get_event(event_id=event_id)
    return event
