from fastapi import APIRouter

from app.api.v1.events import router as events_router


router_v1 = APIRouter(
    prefix="/v1",
)
router_v1.include_router(
    events_router,
    prefix="/events",
    tags=[
        "events",
    ],
)
