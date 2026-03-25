"""
Coursera scraper - free Spanish courses via the public REST API.

Uses api.coursera.org instead of the website to avoid Cloudflare/bot
detection issues in cloud deployments.
"""

import logging
import httpx
from app.schemas import Opportunity, OpportunityType

logger = logging.getLogger(__name__)

BASE_URL = "https://www.coursera.org"
API_URL = "https://api.coursera.org/api/courses.v1"

# Pages to fetch from the catalog (100 courses/page).
# ~6 % of catalog is Spanish → 20 pages ≈ 120 Spanish courses.
_PAGES = 20

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


class CourseraScraper:
    """Fetches free Spanish courses from the Coursera public catalog API."""

    source_name = "Coursera"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        seen_slugs: set[str] = set()

        try:
            with httpx.Client(headers=_HEADERS, timeout=20) as client:
                for page in range(_PAGES):
                    try:
                        r = client.get(
                            API_URL,
                            params={
                                "limit": 100,
                                "start": page * 100,
                                "fields": "name,slug,primaryLanguages,subtitleLanguages,description",
                            },
                        )
                        r.raise_for_status()
                    except Exception as e:
                        logger.error("Coursera API page %s error: %s", page, e)
                        break

                    elements = r.json().get("elements", [])
                    if not elements:
                        break

                    for course in elements:
                        slug = course.get("slug", "")
                        if not slug or slug in seen_slugs:
                            continue

                        primary = course.get("primaryLanguages", [])
                        subtitle = course.get("subtitleLanguages", [])

                        # Keep courses with Spanish as primary or subtitle language
                        if "es" not in primary and "es" not in subtitle:
                            continue

                        seen_slugs.add(slug)
                        name = course.get("name", "").strip()
                        if not name:
                            continue

                        raw_desc = course.get("description") or ""
                        description = raw_desc[:500] if raw_desc else None

                        opportunities.append(
                            Opportunity(
                                title=name,
                                description=description,
                                opportunity_type=OpportunityType.COURSE,
                                provider="Coursera",
                                source_url=f"{BASE_URL}/learn/{slug}",
                                location="Online",
                                is_free=True,
                                tags=["coursera", "gratuito", "online", "español"],
                            )
                        )

        except Exception as e:
            logger.error("Coursera scraper error: %s", e)

        logger.info("Coursera: %s Spanish courses found", len(opportunities))
        return opportunities
