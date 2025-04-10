from pydantic import BaseModel


class EventCategoryOutSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class EventOutSchema(BaseModel):
    # todo:
    name: str

    class Config:
        from_attributes = True


class EventCategoryInSchema(BaseModel):
    name: str
