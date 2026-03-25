"""
Aprende.MX scraper - Portal de cursos gratuitos del Gobierno de México.

Cursos gratuitos en línea impartidos por instituciones públicas mexicanas.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class AprendeMXScraper(BaseScraper):
    """Scrapes free courses from the Mexican government's Aprende.MX portal."""

    BASE_URL = "https://cursos.aprende.gob.mx"
    source_name = "AprendeMX"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        seen_urls = set()
        page = self.new_page()

        try:
            page.goto(f"{self.BASE_URL}/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            for _ in range(4):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            cards = page.query_selector_all("article")
            logger.info("Found %s course cards", len(cards))

            for card in cards:
                try:
                    link = card.query_selector('a[href*="/courses/"]')
                    if not link:
                        continue

                    href = link.get_attribute("href")
                    if not href:
                        continue

                    full_url = (
                        href if href.startswith("http") else f"{self.BASE_URL}{href}"
                    )
                    if full_url in seen_urls:
                        continue
                    seen_urls.add(full_url)

                    # Title from h3/h4 or image alt
                    title = None
                    h_tag = card.query_selector("h3, h4, .course-title, .title")
                    if h_tag:
                        title = h_tag.inner_text().strip()
                    if not title:
                        img = card.query_selector("img")
                        if img:
                            title = img.get_attribute("alt")
                    if not title or len(title) < 5:
                        continue

                    opportunities.append(
                        Opportunity(
                            title=title,
                            description=None,
                            opportunity_type=OpportunityType.COURSE,
                            provider="Gobierno de México",
                            source_url=full_url,
                            location="Online",
                            is_free=True,
                            tags=["aprende.mx", "gobierno de méxico", "gratuito", "online"],
                        )
                    )

                except Exception as e:
                    logger.error("Error processing card: %s", e)
                    continue

            logger.info("Total opportunities: %s", len(opportunities))

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities
