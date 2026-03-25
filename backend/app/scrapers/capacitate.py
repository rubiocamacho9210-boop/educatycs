"""
Capacítate para el Empleo scraper - Fundación Carlos Slim.

Usa la API interna del sitio para obtener cursos.
"""

import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)


class CapacitateScraper(BaseScraper):
    """Scrapes courses from Capacítate para el Empleo via API."""

    BASE_URL = "https://capacitateparaelempleo.org"
    API_URL = "https://besvc.capacitateparaelempleo.org/api"
    source_name = "Capacítate para el Empleo"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()

        try:
            # First visit the site to get proper session/cookies
            page.goto(self.BASE_URL, wait_until="domcontentloaded", timeout=30000)

            # Capture API response
            api_data = []

            def capture_courses(response):
                if "Courses/newCourses" in response.url:
                    try:
                        data = response.json()
                        api_data.extend(data)
                    except Exception:
                        pass

            page.on("response", capture_courses)

            # Reload to trigger API calls
            page.reload(wait_until="networkidle", timeout=30000)

            # Parse captured data
            for course in api_data:
                try:
                    opportunity = self._parse_course(course)
                    if opportunity:
                        opportunities.append(opportunity)
                except Exception:
                    continue

        except Exception as e:
            logger.error("Error: %s", e)

        finally:
            page.close()

        return opportunities

    def _parse_course(self, course: dict) -> Opportunity | None:
        """Parse course data from API response."""
        name = course.get("name")
        course_id = course.get("id")

        if not name or not course_id:
            return None

        # Get sector/category
        sector = course.get("sector", {})
        sector_name = sector.get("name", "General")

        # Build tags
        tags = ["capacitate", "fundación slim", "gratuito"]
        if sector_name:
            tags.append(sector_name.lower())

        # Check if coming soon
        coming_soon = course.get("comingSoon", False)
        if coming_soon:
            tags.append("próximamente")

        return Opportunity(
            title=name,
            description=None,  # API doesn't include description in list
            opportunity_type=OpportunityType.WORKSHOP,
            provider="Fundación Carlos Slim",
            source_url=f"{self.BASE_URL}/cursos/view/{course_id}",
            location="Online",
            is_free=True,
            tags=tags
        )
