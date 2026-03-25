"""
Base scraper class.

Design decisions:
- Synchronous Playwright (simpler to debug, sufficient for this use case)
- Each scraper manages its own browser lifecycle
- Abstract method forces consistent interface
"""

from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright, Browser, Page


class BaseScraper(ABC):
    """Base class for all scrapers."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self._pw_context = None
        self._playwright = None
        self._browser: Browser | None = None

    def __enter__(self):
        self._pw_context = sync_playwright()
        self._playwright = self._pw_context.__enter__()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            self._browser.close()
        if self._pw_context:
            self._pw_context.__exit__(exc_type, exc_val, exc_tb)

    def new_page(self) -> Page:
        """Create a new browser page."""
        if not self._browser:
            raise RuntimeError("Scraper must be used as context manager")
        return self._browser.new_page()

    #: Human-readable name for this source. Must be set by each subclass.
    source_name: str = ""

    @abstractmethod
    def scrape(self) -> list:
        """
        Scrape and return normalized opportunities.
        Must be implemented by each scraper.
        """
        pass
