"""
Conecta Empleo scraper - Fundación Telefónica.

Cursos gratuitos de empleabilidad y habilidades digitales.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class ConectaEmpleoScraper(BaseScraper):
    """Scrapes courses from Conecta Empleo (Fundación Telefónica)."""

    BASE_URL = "https://conectaempleo-formacion.fundaciontelefonica.com"
    source_name = "Conecta Empleo"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            page.goto(f"{self.BASE_URL}/espana", wait_until="networkidle", timeout=30000)

            # Accept cookies if present
            try:
                accept_btn = page.query_selector(
                    'button:has-text("Aceptar"), #onetrust-accept-btn-handler'
                )
                if accept_btn:
                    accept_btn.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass

            # Scroll to load content
            page.evaluate("window.scrollTo(0, 1000)")
            page.wait_for_timeout(2000)

            # Find course links
            links = page.query_selector_all('a[href*="/web/"], a[href*="curso"]')

            seen = set()
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href or href in seen:
                        continue

                    # Skip non-course links
                    if any(skip in href.lower() for skip in ["login", "registro", "candidato"]):
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
        """Parse a course link."""
        text = link.inner_text().strip()

        if not text or len(text) < 5:
            return None

        # Get title from first line
        lines = text.split("\n")
        title = lines[0].strip()

        # Skip generic links
        if title.lower() in ["ver más", "acceder", "registro", "inscripciones abiertas"]:
            return None

        if len(title) < 5:
            return None

        # Get description if available
        description = lines[1].strip() if len(lines) > 1 else None

        # Build full URL
        if href.startswith("/"):
            full_url = f"{self.BASE_URL}{href}"
        else:
            full_url = href

        return Opportunity(
            title=title,
            description=description[:200] if description else None,
            opportunity_type=OpportunityType.COURSE,
            provider="Fundación Telefónica",
            source_url=full_url,
            location="Online",
            is_free=True,
            tags=["telefónica", "conecta empleo", "empleabilidad", "gratuito"]
        )
