import http
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

from app.services.event import get_event_service, EventService
from .schemas import (
    EventCategoryOutSchema,
    EventOutSchema,
    EventCategoryInSchema,
    EventFilterSchema,
    EventCategoryFilterSchema,
)

router = APIRouter()


# CATEGORIES
@router.get("/categories", response_model=list[EventCategoryOutSchema])
async def get_all_categories(
    filters: Annotated[EventCategoryFilterSchema, Query()],
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    categories = await event_service.get_categories(
        **filters.dict(exclude_unset=True, by_alias=True)
    )
    return categories


@router.post(
    "/categories",
    response_model=EventCategoryOutSchema,
    responses={
        http.HTTPStatus.BAD_REQUEST: {
            "content": {"application/json": {"example": {"detail": "Category already exists."}}},
            "description": "Category is still referenced from events table.",
        }
    },
)
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


@router.delete(
    "/categories/{category_name}",
    response_model=None,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    status_code=http.HTTPStatus.NO_CONTENT,
    responses={
        http.HTTPStatus.BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {"detail": "Category=X is still referenced from events table."}
                }
            },
            "description": "Category is still referenced from events table.",
        }
    },
)
async def delete_category(
    category_name: str,
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    try:
        await event_service.delete_category(name=category_name)
    except IntegrityError:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail=f"Category={category_name} is still referenced from events table.",
        )
    return JSONResponse(status_code=http.HTTPStatus.NO_CONTENT, content="")


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
