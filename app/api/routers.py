from fastapi import APIRouter

from app.api.v1.event_category import router as event_category_router


router_v1 = APIRouter(
    prefix="/v1",
)
router_v1.include_router(event_category_router, prefix="/categories", tags=["categories"])
