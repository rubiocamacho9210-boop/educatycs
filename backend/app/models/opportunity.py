"""
SQLAlchemy model for Opportunity.
"""

from datetime import datetime, date, timezone
from sqlalchemy import String, Boolean, Date, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OpportunityModel(Base):
    """Database model for educational opportunities."""

    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Core fields
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    opportunity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(200), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # scraper name

    # Optional fields
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_free: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Opportunity {self.id}: {self.title[:30]}...>"
