import datetime

from pydantic import BaseModel


class EventCategoryOutSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class EventOutSchema(BaseModel):
    id: int
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    venue: str
    total_tickets: int
    available_tickets: int
    price: float
    category: EventCategoryOutSchema
    image_url: str
    is_published: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class EventCategoryInSchema(BaseModel):
    name: str
