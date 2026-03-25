"""
One-off migration utility from the local SQLite catalog to PostgreSQL.

Usage:
  SQLITE_DATABASE_URL=sqlite:///educatycs.db \
  DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname \
  python scripts/migrate_sqlite_to_postgres.py
"""

from __future__ import annotations

import os
from collections.abc import Iterable

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, normalize_database_url
from app.models import OpportunityModel


def chunked(items: list[OpportunityModel], size: int) -> Iterable[list[OpportunityModel]]:
    for index in range(0, len(items), size):
        yield items[index:index + size]


def clone_opportunity(opportunity: OpportunityModel) -> OpportunityModel:
    return OpportunityModel(
        title=opportunity.title,
        description=opportunity.description,
        opportunity_type=opportunity.opportunity_type,
        provider=opportunity.provider,
        source_url=opportunity.source_url,
        source=opportunity.source,
        location=opportunity.location,
        start_date=opportunity.start_date,
        end_date=opportunity.end_date,
        is_free=opportunity.is_free,
        tags=opportunity.tags,
        created_at=opportunity.created_at,
        updated_at=opportunity.updated_at,
        is_active=opportunity.is_active,
    )


def main() -> None:
    source_url = normalize_database_url(
        os.environ.get("SQLITE_DATABASE_URL", "sqlite:///educatycs.db")
    )
    target_url = os.environ.get("DATABASE_URL")
    if not target_url:
        raise RuntimeError("DATABASE_URL is required and must point to PostgreSQL")
    target_url = normalize_database_url(target_url)

    source_engine = create_engine(source_url, connect_args={"check_same_thread": False})
    target_engine = create_engine(target_url, pool_pre_ping=True)
    Base.metadata.create_all(bind=target_engine)

    source_session_factory = sessionmaker(bind=source_engine)
    target_session_factory = sessionmaker(bind=target_engine)

    with Session(source_engine) as source_session:
        opportunities = source_session.scalars(
            select(OpportunityModel).order_by(OpportunityModel.id.asc())
        ).all()

    inserted = 0
    updated = 0

    with Session(target_engine) as target_session:
        existing = {
            row.source_url: row
            for row in target_session.scalars(select(OpportunityModel)).all()
        }

        for batch in chunked(opportunities, 250):
            for source_row in batch:
                current = existing.get(source_row.source_url)
                if current is None:
                    current = clone_opportunity(source_row)
                    target_session.add(current)
                    existing[source_row.source_url] = current
                    inserted += 1
                    continue

                current.title = source_row.title
                current.description = source_row.description
                current.opportunity_type = source_row.opportunity_type
                current.provider = source_row.provider
                current.source = source_row.source
                current.location = source_row.location
                current.start_date = source_row.start_date
                current.end_date = source_row.end_date
                current.is_free = source_row.is_free
                current.tags = source_row.tags
                current.created_at = source_row.created_at
                current.updated_at = source_row.updated_at
                current.is_active = source_row.is_active
                updated += 1

            target_session.commit()

    print(
        f"Migration complete. Source rows: {len(opportunities)} | inserted: {inserted} | updated: {updated}"
    )


if __name__ == "__main__":
    main()
