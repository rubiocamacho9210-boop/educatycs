"""
UNAM MOOC scraper.

Cursos gratuitos de la UNAM en Coursera.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper
from pydantic import TypeAdapter, HttpUrl

logger = logging.getLogger(__name__)


class UNAMScraper(BaseScraper):
    """Scrapes courses from UNAM MOOC."""

    BASE_URL = "https://mooc.unam.mx"
    source_name = "UNAM MOOC"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        seen_urls = set()
        page = self.new_page()

        try:
            page.goto(f"{self.BASE_URL}/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

            course_links = page.query_selector_all("a[href*='/learn/']")

            logger.info("Found %s course links", len(course_links))

            for link in course_links:
                try:
                    href = link.get_attribute("href")
                    if not href or href in seen_urls:
                        continue
                    seen_urls.add(href)

                    title = link.inner_text().strip()
                    if not title or len(title) < 5:
                        continue

                    url_validator = TypeAdapter(HttpUrl)
                    validated_url = url_validator.validate_python(href)

                    opportunities.append(
                        Opportunity(
                            title=title,
                            description=None,
                            opportunity_type=OpportunityType.COURSE,
                            provider="UNAM",
                            source_url=validated_url,
                            location="Online",
                            is_free=True,
                            tags=["unam", "gratuito", "méxico", "mooc"],
                        )
                    )

                except Exception as e:
                    logger.error("Error processing link: %s", e)
                    continue

            logger.info("Total opportunities: %s", len(opportunities))

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities
