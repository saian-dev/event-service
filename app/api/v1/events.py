import http
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.event import get_event_service, EventService
from app.api.utils import pagination_params
from .schemas import EventCategoryOutSchema, EventOutSchema, EventCategoryInSchema

router = APIRouter()


# CATEGORIES
@router.get("/categories", response_model=list[EventCategoryOutSchema])
async def get_all_categories(
    pagination: Annotated[dict, Depends(pagination_params)],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    categories = await event_service.get_categories(
        limit=pagination["limit"], offset=pagination["offset"]
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
    pagination: Annotated[dict, Depends(pagination_params)],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    # todo: add filters, proper schema
    events = await event_service.get_events(limit=pagination["limit"], offset=pagination["offset"])
    return events
