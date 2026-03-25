"""
Pydantic schemas for educational opportunities.

Design decisions:
- Single model for all opportunity types (course, workshop, scholarship)
- Optional fields for flexibility across different sources
- source_url for traceability back to original posting
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class OpportunityType(str, Enum):
    COURSE = "course"
    WORKSHOP = "workshop"
    SCHOLARSHIP = "scholarship"
    EVENT = "event"
    OTHER = "other"


class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = None
    opportunity_type: OpportunityType
    provider: str  # e.g., "Coursera", "UADY", "CONACYT"
    source_url: HttpUrl

    # Optional fields - not all sources provide these
    location: Optional[str] = None  # "Online", "Mérida", etc.
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_free: Optional[bool] = None
    tags: list[str] = Field(default_factory=list)


class OpportunityCreate(OpportunityBase):
    """Payload to manually create an opportunity."""

    source: str = "manual"


class OpportunityUpdate(BaseModel):
    """Partial update payload for an existing opportunity."""

    title: Optional[str] = None
    description: Optional[str] = None
    opportunity_type: Optional[OpportunityType] = None
    provider: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    source: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_free: Optional[bool] = None
    tags: Optional[list[str]] = None


class Opportunity(OpportunityBase):
    """Normalized educational opportunity from any source."""

    id: int | None = None
    source: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 42,
                "title": "Introducción a Python",
                "description": "Curso básico de programación",
                "opportunity_type": "course",
                "provider": "Coursera",
                "source_url": "https://coursera.org/learn/python",
                "location": "Online",
                "is_free": True,
                "tags": ["programación", "tecnología"],
            }
        }
    )
