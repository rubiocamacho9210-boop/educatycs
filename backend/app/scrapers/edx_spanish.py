"""
edX Spanish courses scraper.

Cursos gratuitos en español de universidades reconocidas.
"""

import logging
import re
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class EdxSpanishScraper(BaseScraper):
    """Scrapes free Spanish courses from edX."""

    BASE_URL = "https://www.edx.org"
    SEARCH_URL = f"{BASE_URL}/search?q=&language=Spanish&price=Free"
    source_name = "edX"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            page.goto(self.SEARCH_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            # Scroll to load more content
            for _ in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Find course links (exclude category pages)
            links = page.query_selector_all('a[href*="/learn/"][href*="?index="]')

            seen = set()
            for link in links:
                try:
                    href = link.get_attribute("href")
                    # Clean URL
                    clean_href = href.split("?")[0] if href else None

                    if not clean_href or clean_href in seen:
                        continue
                    seen.add(clean_href)

                    opportunity = self._parse_link(link, clean_href)
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
        text = link.inner_text().strip()

        if not text or len(text) < 5:
            return None

        # Parse the text format: "Course\nTitle\nInstitution | Type"
        lines = [line_text.strip() for line_text in text.split("\n") if line_text.strip()]

        if len(lines) < 2:
            return None

        # First line is usually "Course", second is title
        title = None
        provider = "edX"

        for line in lines:
            if line.lower() == "course":
                continue
            if not title:
                title = line
            elif "|" in line or "University" in line or "Institut" in line:
                # This is the provider line
                provider = line.split("|")[0].strip()
                break

        if not title:
            return None

        # Clean title
        title = re.sub(r'\s+', ' ', title).strip()

        # Build full URL
        full_url = f"{self.BASE_URL}{href}" if href.startswith("/") else href

        return Opportunity(
            title=title,
            description=None,
            opportunity_type=OpportunityType.COURSE,
            provider=provider,
            source_url=full_url,
            location="Online",
            is_free=True,
            tags=["edx", "español", "universidad", "gratuito"]
        )
