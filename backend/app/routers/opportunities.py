"""
API endpoints for educational opportunities.

Endpoints:
- GET /opportunities/ - List from database (fast)
- POST /opportunities/refresh - Scrape and update database (blocking)
- POST /opportunities/refresh-async - Scrape in background (non-blocking)
- GET /opportunities/sources - List available sources
- GET /opportunities/scheduler - Get scheduler status
"""

import logging
from datetime import datetime, timezone
from secrets import compare_digest

from fastapi import APIRouter, HTTPException, Query, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import or_, String
from sqlalchemy.exc import IntegrityError

from app.config import get_settings
from app.database import get_db
from app.models import OpportunityModel
from app.schemas import Opportunity, OpportunityCreate, OpportunityUpdate
from app.scheduler import get_scheduler_status, trigger_refresh_now
from app.scrapers import (
    CourseraScraper,
    CapacitateScraper,
    GoogleActivateScraper,
    ConectaEmpleoScraper,
    EdxSpanishScraper,
    KhanAcademyScraper,
    SantanderScraper,
    UNAMScraper,
    IdiomaScraper,
    BecasScraper,
)

router = APIRouter(prefix="/opportunities", tags=["opportunities"])
settings = get_settings()
logger = logging.getLogger("educatycs.router")

# Registry of available scrapers
SCRAPERS = {
    "capacitate": CapacitateScraper,
    "google": GoogleActivateScraper,
    "conecta_empleo": ConectaEmpleoScraper,
    "edx": EdxSpanishScraper,
    "coursera": CourseraScraper,
    "khan": KhanAcademyScraper,
    "santander": SantanderScraper,
    "unam": UNAMScraper,
    "idiomas": IdiomaScraper,
    "becas": BecasScraper,
}


def require_admin_key(
    x_admin_key: str | None = Header(default=None, alias="X-Admin-Key"),
) -> None:
    """Protect admin-only CRUD actions."""
    if not settings.admin_api_key:
        raise HTTPException(
            status_code=503,
            detail="ADMIN_API_KEY is not configured on the server",
        )
    if not x_admin_key or not compare_digest(x_admin_key, settings.admin_api_key):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")


@router.post("/", response_model=Opportunity, status_code=201)
def create_opportunity(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key),
) -> Opportunity:
    """Create a manual opportunity entry."""
    new_opp = OpportunityModel(
        title=payload.title,
        description=payload.description,
        opportunity_type=payload.opportunity_type.value,
        provider=payload.provider,
        source_url=str(payload.source_url),
        source=payload.source,
        location=payload.location,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_free=payload.is_free,
        tags=payload.tags,
        is_active=True,
    )

    db.add(new_opp)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Opportunity already exists for URL: {payload.source_url}",
        )
    db.refresh(new_opp)
    return _model_to_schema(new_opp)


@router.get("/", response_model=list[Opportunity])
def list_opportunities(
    source: str | None = Query(default=None, description="Filter by source"),
    search: str | None = Query(default=None, description="Search in title"),
    is_free: bool | None = Query(default=None, description="Filter by free courses"),
    opportunity_type: str | None = Query(
        default=None,
        description="Filter by type (course, scholarship, workshop, event)",
    ),
    tag: str | None = Query(default=None, description="Filter by tag"),
    limit: int = Query(default=100, le=500, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Skip results"),
    db: Session = Depends(get_db),
) -> list[Opportunity]:
    """
    List opportunities from database.

    Use POST /opportunities/refresh to update data from sources.
    """
    query = db.query(OpportunityModel).filter(OpportunityModel.is_active.is_(True))

    # Apply filters
    if source:
        query = query.filter(OpportunityModel.source == source)

    if search:
        query = query.filter(
            or_(
                OpportunityModel.title.ilike(f"%{search}%"),
                OpportunityModel.description.ilike(f"%{search}%"),
            )
        )

    if is_free is not None:
        query = query.filter(OpportunityModel.is_free == is_free)

    if opportunity_type:
        query = query.filter(OpportunityModel.opportunity_type == opportunity_type)

    if tag:
        query = query.filter(OpportunityModel.tags.cast(String).like(f'%"{tag}"%'))

    # Order by most recent
    query = query.order_by(OpportunityModel.updated_at.desc())

    # Pagination
    results = query.offset(offset).limit(limit).all()

    # Convert to Pydantic models
    return [_model_to_schema(r) for r in results]


@router.get("/total")
def count_opportunities(
    source: str | None = Query(default=None),
    search: str | None = Query(default=None),
    opportunity_type: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    """Return total count of opportunities matching the given filters."""
    query = db.query(OpportunityModel).filter(OpportunityModel.is_active.is_(True))

    if source:
        query = query.filter(OpportunityModel.source == source)
    if search:
        query = query.filter(
            or_(
                OpportunityModel.title.ilike(f"%{search}%"),
                OpportunityModel.description.ilike(f"%{search}%"),
            )
        )
    if opportunity_type:
        query = query.filter(OpportunityModel.opportunity_type == opportunity_type)
    if tag:
        query = query.filter(OpportunityModel.tags.cast(String).like(f'%"{tag}"%'))

    return {"total": query.count()}


def _get_opportunity_by_id(
    opportunity_id: int,
    db: Session = Depends(get_db),
) -> Opportunity:
    """
    Get a single opportunity by ID.
    """
    opportunity = (
        db.query(OpportunityModel)
        .filter(
            OpportunityModel.id == opportunity_id, OpportunityModel.is_active.is_(True)
        )
        .first()
    )

    if not opportunity:
        raise HTTPException(
            status_code=404, detail=f"Opportunity with id {opportunity_id} not found"
        )

    return _model_to_schema(opportunity)


@router.patch("/{opportunity_id}", response_model=Opportunity)
def update_opportunity(
    opportunity_id: int,
    payload: OpportunityUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key),
) -> Opportunity:
    """Partially update an opportunity by ID."""
    opportunity = (
        db.query(OpportunityModel)
        .filter(
            OpportunityModel.id == opportunity_id,
            OpportunityModel.is_active.is_(True),
        )
        .first()
    )
    if not opportunity:
        raise HTTPException(
            status_code=404, detail=f"Opportunity with id {opportunity_id} not found"
        )

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return _model_to_schema(opportunity)

    if "opportunity_type" in updates and updates["opportunity_type"] is not None:
        updates["opportunity_type"] = updates["opportunity_type"].value
    if "source_url" in updates and updates["source_url"] is not None:
        updates["source_url"] = str(updates["source_url"])

    for field, value in updates.items():
        setattr(opportunity, field, value)
    opportunity.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Another opportunity already uses the provided source_url",
        )
    db.refresh(opportunity)
    return _model_to_schema(opportunity)


@router.delete("/{opportunity_id}", status_code=204)
def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key),
) -> None:
    """Hard-delete an opportunity by ID."""
    opportunity = (
        db.query(OpportunityModel)
        .filter(OpportunityModel.id == opportunity_id)
        .first()
    )
    if not opportunity:
        raise HTTPException(
            status_code=404, detail=f"Opportunity with id {opportunity_id} not found"
        )

    db.delete(opportunity)
    db.commit()
    return None


@router.post("/refresh")
def refresh_opportunities(
    source: str = Query(
        default="all",
        description="Source to refresh. Use 'all' for all sources.",
    ),
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_key),
) -> dict:
    """
    Scrape sources and update database.

    This may take a while depending on the source.
    """
    if source != "all" and source not in SCRAPERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown source: {source}. Available: {list(SCRAPERS.keys()) + ['all']}",
        )

    sources_to_scrape = SCRAPERS.keys() if source == "all" else [source]
    results = {"refreshed": [], "errors": [], "total_new": 0, "total_updated": 0}

    for src_name in sources_to_scrape:
        scraper_class = SCRAPERS[src_name]
        try:
            with scraper_class() as scraper:
                opportunities = scraper.scrape()

                new_count, updated_count = _save_opportunities(
                    db, opportunities, src_name
                )

                results["refreshed"].append(src_name)
                results["total_new"] += new_count
                results["total_updated"] += updated_count

                logger.info("[%s] New: %s, Updated: %s", src_name, new_count, updated_count)

        except Exception as e:
            results["errors"].append({"source": src_name, "error": str(e)})
            logger.error("[%s] Error: %s", src_name, e)

    return results


@router.get("/sources")
def list_sources(db: Session = Depends(get_db)) -> dict:
    """List available sources and their stats."""
    sources_info = {}

    for source_name in SCRAPERS.keys():
        count = (
            db.query(OpportunityModel)
            .filter(
                OpportunityModel.source == source_name,
                OpportunityModel.is_active.is_(True),
            )
            .count()
        )

        sources_info[source_name] = {
            "name": SCRAPERS[source_name].source_name,
            "count": count,
        }

    total = (
        db.query(OpportunityModel).filter(OpportunityModel.is_active.is_(True)).count()
    )

    return {
        "sources": sources_info,
        "total_opportunities": total,
        "tip": "Use POST /opportunities/refresh?source=all to update data",
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)) -> dict:
    """Get database statistics."""
    total = db.query(OpportunityModel).count()
    active = (
        db.query(OpportunityModel).filter(OpportunityModel.is_active.is_(True)).count()
    )
    free = (
        db.query(OpportunityModel)
        .filter(OpportunityModel.is_free.is_(True), OpportunityModel.is_active.is_(True))
        .count()
    )

    # Count by source
    by_source = {}
    for source_name in SCRAPERS.keys():
        by_source[source_name] = (
            db.query(OpportunityModel)
            .filter(
                OpportunityModel.source == source_name,
                OpportunityModel.is_active.is_(True),
            )
            .count()
        )

    # Most recent update
    latest = (
        db.query(OpportunityModel).order_by(OpportunityModel.updated_at.desc()).first()
    )

    return {
        "total": total,
        "active": active,
        "free": free,
        "by_source": by_source,
        "last_updated": latest.updated_at.isoformat() if latest else None,
    }


def _save_opportunities(
    db: Session, opportunities: list[Opportunity], source: str
) -> tuple[int, int]:
    """Save opportunities to database. Returns (new_count, updated_count)."""
    new_count = 0
    updated_count = 0

    for opp in opportunities:
        # Check if exists by URL
        existing = (
            db.query(OpportunityModel)
            .filter(OpportunityModel.source_url == str(opp.source_url))
            .first()
        )

        if existing:
            # Update existing
            existing.title = opp.title
            existing.description = opp.description
            existing.opportunity_type = opp.opportunity_type.value
            existing.provider = opp.provider
            existing.location = opp.location
            existing.start_date = opp.start_date
            existing.end_date = opp.end_date
            existing.is_free = opp.is_free
            existing.tags = opp.tags
            existing.updated_at = datetime.now(timezone.utc)
            existing.is_active = True
            updated_count += 1
        else:
            # Create new
            new_opp = OpportunityModel(
                title=opp.title,
                description=opp.description,
                opportunity_type=opp.opportunity_type.value,
                provider=opp.provider,
                source_url=str(opp.source_url),
                source=source,
                location=opp.location,
                start_date=opp.start_date,
                end_date=opp.end_date,
                is_free=opp.is_free,
                tags=opp.tags,
            )
            db.add(new_opp)
            new_count += 1

    db.commit()
    return new_count, updated_count


def _model_to_schema(model: OpportunityModel) -> Opportunity:
    """Convert SQLAlchemy model to Pydantic schema."""
    from app.schemas import OpportunityType

    return Opportunity(
        id=model.id,
        title=model.title,
        description=model.description,
        opportunity_type=OpportunityType(model.opportunity_type),
        provider=model.provider,
        source_url=model.source_url,
        source=model.source,
        location=model.location,
        start_date=model.start_date,
        end_date=model.end_date,
        is_free=model.is_free,
        tags=model.tags or [],
    )


# ============== Scheduler Endpoints ==============


@router.get("/scheduler")
def scheduler_status() -> dict:
    """
    Get background scheduler status.

    Shows if automatic refresh is running and next scheduled run.
    """
    return get_scheduler_status()


@router.post("/refresh-async")
def refresh_async(_: None = Depends(require_admin_key)) -> dict:
    """
    Trigger a background refresh (non-blocking).

    Returns immediately while scraping runs in background.
    Use GET /opportunities/scheduler to check status.
    """
    return trigger_refresh_now()


@router.get("/{opportunity_id}", response_model=Opportunity)
def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
) -> Opportunity:
    """Get a single opportunity by ID."""
    return _get_opportunity_by_id(opportunity_id, db)
