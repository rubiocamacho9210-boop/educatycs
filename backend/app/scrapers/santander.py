"""
Santander Open Academy scraper.

Becas y cursos gratuitos de Santander.
"""

import html
import json
import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper
from pydantic import HttpUrl, TypeAdapter

logger = logging.getLogger(__name__)


class SantanderScraper(BaseScraper):
    """Scrapes courses from Santander Open Academy."""

    BASE_URL = "https://www.santanderopenacademy.com"
    source_name = "Santander Open Academy"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        seen_urls = set()
        page = self.new_page()

        try:
            page.goto(
                f"{self.BASE_URL}/es/courses-quick-access.html",
                wait_until="networkidle",
                timeout=30000,
            )
            page.wait_for_timeout(3000)

            for _ in range(5):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1500)

            cards = page.query_selector_all("soa-card")

            for card in cards:
                try:
                    soa_item = card.get_attribute("soa-item")
                    if not soa_item:
                        continue

                    data = json.loads(html.unescape(soa_item))
                    course_id = data.get("externalIdentifier")

                    if not course_id:
                        continue

                    title = data.get("name", "").strip()
                    if not title or len(title) < 5:
                        continue

                    course_url = (
                        f"https://app.santanderopenacademy.com/es/course/{course_id}"
                    )

                    if course_url in seen_urls:
                        continue
                    seen_urls.add(course_url)

                    url_validator = TypeAdapter(HttpUrl)
                    validated_url = url_validator.validate_python(course_url)

                    description = data.get("description", "")
                    clean_desc = None
                    if description:
                        clean_desc = (
                            description[:500] if len(description) > 500 else description
                        )
                        clean_desc = (
                            clean_desc.replace("<div>", "")
                            .replace("</div>", "")
                            .replace("<p>", "")
                            .replace("</p>", "")
                        )
                        clean_desc = clean_desc.strip()

                    provider = data.get("provider", "Santander Open Academy")

                    opportunities.append(
                        Opportunity(
                            title=title,
                            description=clean_desc,
                            opportunity_type=OpportunityType.COURSE,
                            provider=provider,
                            source_url=validated_url,
                            location="Online",
                            is_free=True,
                            tags=["santander", "gratuito", "español"],
                        )
                    )

                except Exception:
                    continue

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities
