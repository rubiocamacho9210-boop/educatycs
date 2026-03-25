"""
Khan Academy scraper - Cursos gratuitos en español.

Matemáticas, ciencias, computación y más.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class KhanAcademyScraper(BaseScraper):
    """Scrapes courses from Khan Academy in Spanish."""

    BASE_URL = "https://es.khanacademy.org"
    source_name = "Khan Academy"

    # Categories to scrape
    CATEGORIES = [
        "/computing",
        "/math",
        "/science",
        "/economics-finance-domain",
        "/humanities",
    ]

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            for category in self.CATEGORIES:
                try:
                    url = f"{self.BASE_URL}{category}"
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    page.wait_for_timeout(1000)

                    # Find course links within this category
                    links = page.query_selector_all(f'a[href*="{category}/"]')

                    seen = set()
                    for link in links:
                        try:
                            href = link.get_attribute("href")
                            if not href or href in seen:
                                continue

                            # Skip if it's just the category page
                            if href.rstrip("/") == category:
                                continue

                            seen.add(href)

                            opportunity = self._parse_link(link, href, category)
                            if opportunity:
                                opportunities.append(opportunity)
                        except Exception:
                            continue

                except Exception as e:
                    logger.error("Error in %s: %s", category, e)
                    continue

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities

    def _parse_link(self, link, href: str, category: str) -> Opportunity | None:
        """Parse a course link."""
        text = link.inner_text().strip()

        if not text or len(text) < 3:
            return None

        # Get title (first part before colon or newline)
        title = text.split("\n")[0].split(":")[0].strip()

        if len(title) < 3:
            return None

        # Build full URL
        full_url = href if href.startswith("http") else f"{self.BASE_URL}{href}"

        # Determine category tag
        category_tag = category.strip("/").split("/")[0]
        category_names = {
            "computing": "programación",
            "math": "matemáticas",
            "science": "ciencias",
            "economics-finance-domain": "economía",
            "humanities": "humanidades",
        }

        tags = ["khan academy", "gratuito", "español"]
        if category_tag in category_names:
            tags.append(category_names[category_tag])

        return Opportunity(
            title=title,
            description=None,
            opportunity_type=OpportunityType.COURSE,
            provider="Khan Academy",
            source_url=full_url,
            location="Online",
            is_free=True,
            tags=tags,
        )
