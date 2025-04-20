import datetime

from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    limit: int = Field(100)
    offset: int = Field(0)


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


class EventFilterSchema(PaginationSchema):
    is_published: bool | None = Field(None, description="Is published?")
    category: str | None = Field(
        None, description="Category of event", serialization_alias="category_id"
    )
    start_date: datetime.datetime = Field(None, description="Start date of event")
    end_date: datetime.datetime = Field(None, description="End date of event")
