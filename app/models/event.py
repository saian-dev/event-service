import datetime

from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, Float, Index
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    venue: Mapped[str] = mapped_column(String(255), nullable=False)
    total_tickets: Mapped[int] = mapped_column(Integer, nullable=False)
    available_tickets: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = relationship("EventCategory", back_populates="events")
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("idx_start_date_venue", start_date, venue),
        Index("idx_is_published_start_date", is_published, start_date),
    )

    def __repr__(self):
        return f"Event: id={self.id}, title='{self.title}', start_date='{self.start_date}'"


class EventCategory(Base):
    __tablename__ = "event_categories"

    name: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    events: Mapped["Event"] = relationship("Event", back_populates="categories")

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    def __repr__(self):
        return f"EventCategory: {self.name}"
