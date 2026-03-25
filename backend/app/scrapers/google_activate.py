"""
Google Grow / Actívate scraper - Cursos gratuitos de Google en español.

Extrae cursos de Skillshop y Coursera listados en grow.google/intl/es/
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class GoogleActivateScraper(BaseScraper):
    """Scrapes courses from Google Grow (Spanish)."""

    BASE_URL = "https://grow.google/intl/es/courses-and-tools/"
    source_name = "Google Actívate"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            page.goto(self.BASE_URL, wait_until="networkidle", timeout=30000)

            # Scroll to load all content
            for _ in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Find course links (Skillshop and Coursera)
            links = page.query_selector_all(
                'a[href*="skillshop"], a[href*="coursera.org"]'
            )

            seen = set()
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href or href in seen:
                        continue
                    seen.add(href)

                    opportunity = self._parse_link(link, href)
                    if opportunity:
                        opportunities.append(opportunity)
                except Exception:
                    continue

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities

    def _parse_link(self, link, href: str) -> Opportunity | None:
        """Parse a course link element."""
        # Get text from the link and nearby elements
        text = link.inner_text().strip()

        if not text or len(text) < 5:
            return None

        # Split title and description (usually separated by newline)
        parts = text.split("\n")
        title = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else None

        # Skip if title is too short or generic
        if len(title) < 5 or title.lower() in ["ver más", "más información", "explorar"]:
            return None

        # Determine provider based on URL
        if "skillshop" in href:
            provider = "Google Skillshop"
        elif "coursera" in href:
            provider = "Google (via Coursera)"
        else:
            provider = "Google"

        # Determine if it's a certificate
        is_certificate = "certificad" in title.lower() or "certificate" in href.lower()

        tags = ["google", "gratuito", "español"]
        if is_certificate:
            tags.append("certificación")
        if "ia" in title.lower() or "ai" in title.lower():
            tags.append("inteligencia artificial")
        if "marketing" in title.lower():
            tags.append("marketing digital")
        if "datos" in title.lower() or "data" in title.lower():
            tags.append("datos")

        return Opportunity(
            title=title,
            description=description[:200] if description else None,
            opportunity_type=OpportunityType.WORKSHOP,
            provider=provider,
            source_url=href,
            location="Online",
            is_free=True,
            tags=tags
        )
