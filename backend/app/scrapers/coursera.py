"""
Coursera scraper - free courses with Spanish subtitles/content.

Searches for courses relevant to education and employment.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class CourseraScraper(BaseScraper):
    """Scrapes free courses from Coursera."""

    BASE_URL = "https://www.coursera.org"
    source_name = "Coursera"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            # Search for free courses
            url = f"{self.BASE_URL}/courses?query=free&language=Spanish"
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            # Scroll to load content
            for _ in range(2):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Find course links
            links = page.query_selector_all('a[href*="/learn/"]')

            seen = set()
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href or href in seen:
                        continue

                    # Clean URL
                    clean_href = href.split("?")[0]
                    if clean_href in seen:
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
        """Parse a course link."""
        text = link.inner_text().strip()

        if not text or len(text) < 3:
            return None

        # Get just the title (first line usually)
        title = text.split("\n")[0].strip()

        if len(title) < 3:
            return None

        # Build full URL
        full_url = f"{self.BASE_URL}{href}" if href.startswith("/") else href

        return Opportunity(
            title=title,
            description=None,
            opportunity_type=OpportunityType.COURSE,
            provider="Coursera",
            source_url=full_url,
            location="Online",
            is_free=True,
            tags=["coursera", "gratuito", "online"]
        )
