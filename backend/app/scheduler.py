"""
Background scheduler for automatic data refresh.

Uses APScheduler to run scrapers periodically without blocking the API.
"""

import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.database import SessionLocal
from app.models import OpportunityModel
from app.scrapers import (
    CapacitateScraper,
    GoogleActivateScraper,
    ConectaEmpleoScraper,
    EdxSpanishScraper,
    CourseraScraper,
    KhanAcademyScraper,
    SantanderScraper,
    UNAMScraper,
)

# Scheduler instance
scheduler = BackgroundScheduler()
logger = logging.getLogger("educatycs.scheduler")

# Registry of scrapers
SCRAPERS = {
    "capacitate": CapacitateScraper,
    "google": GoogleActivateScraper,
    "conecta_empleo": ConectaEmpleoScraper,
    "edx": EdxSpanishScraper,
    "coursera": CourseraScraper,
    "khan": KhanAcademyScraper,
    "santander": SantanderScraper,
    "unam": UNAMScraper,
}


def refresh_all_sources():
    """
    Job that refreshes all sources.
    Runs in background without blocking the API.
    """
    logger.info("Starting refresh at %s", datetime.now(timezone.utc).isoformat())

    db = SessionLocal()
    total_new = 0
    total_updated = 0

    for name, scraper_class in SCRAPERS.items():
        try:
            logger.info("Scraping %s...", name)
            with scraper_class() as scraper:
                opportunities = scraper.scrape()

                new_count, updated_count = _save_opportunities(db, opportunities, name)
                total_new += new_count
                total_updated += updated_count

                logger.info("%s: %s new, %s updated", name, new_count, updated_count)

        except Exception as e:
            logger.error("%s error: %s", name, e)
            continue

    db.close()
    logger.info("Finished. Total: %s new, %s updated", total_new, total_updated)


def _save_opportunities(db, opportunities, source: str) -> tuple[int, int]:
    """Save opportunities to database."""
    new_count = 0
    updated_count = 0

    for opp in opportunities:
        existing = (
            db.query(OpportunityModel)
            .filter(OpportunityModel.source_url == str(opp.source_url))
            .first()
        )

        if existing:
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
            new_opp = OpportunityModel(
                title=opp.title,
                description=opp.description,
                opportunity_type=opp.opportunity_type.value,
                provider=opp.provider,
                source_url=str(opp.source_url),
                source=source,
                location=opp.location,
                is_free=opp.is_free,
                tags=opp.tags,
            )
            db.add(new_opp)
            new_count += 1

    db.commit()
    return new_count, updated_count


def start_scheduler(interval_hours: int = 6):
    """
    Start the background scheduler.

    Args:
        interval_hours: How often to refresh data (default: every 6 hours)
    """
    scheduler.add_job(
        refresh_all_sources,
        trigger=IntervalTrigger(hours=interval_hours),
        id="refresh_all_sources",
        name="Refresh all educational opportunities",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Started. Will refresh every %s hours.", interval_hours)


def stop_scheduler():
    """Stop the background scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Stopped.")


def get_scheduler_status() -> dict:
    """Get scheduler status and next run time."""
    job = scheduler.get_job("refresh_all_sources")

    if not job:
        return {"running": False, "next_run": None}

    return {
        "running": scheduler.running,
        "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
        "job_name": job.name,
    }


def trigger_refresh_now():
    """Trigger an immediate refresh (non-blocking)."""
    if not scheduler.running:
        scheduler.start()

    scheduler.add_job(
        refresh_all_sources,
        id="manual_refresh",
        name="Manual refresh",
        replace_existing=True,
    )
    return {"status": "Refresh started in background"}
