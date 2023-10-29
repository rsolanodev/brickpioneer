from bs4 import BeautifulSoup, Tag

from brickpioneer import models
from brickpioneer.scrapers.base import BaseScraper


class Metrovacesa(BaseScraper):
    """
    Scraper class for fetching promotions from the Metrovacesa website.
    Example: https://metrovacesa.com/promociones/valencia/
    """

    base_url: str = "https://metrovacesa.com"

    @property
    def promotions_url(self) -> str:
        return f"{self.base_url}/promociones/{self.province}/"

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        return soup.find(id="cartas-promociones")

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        return parent.find_all("div", recursive=False)

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Extracts the promotion details from the given HTML element.
        """
        link = child.find("a")
        promotion = {
            "developer": self.__class__.__name__,
            "province": self.province_display,
            "city": child.get("data-poblacionname", None),
            "price_min": self._get_promotion_price(child),
            "name": child.get("data-map-title", None),
            "url": link.get("href") if link else None,
        }
        return models.Promotion(**promotion)

    def _get_promotion_price(self, child: Tag) -> float | None:
        """
        Gets and parse the price from the given HTML element.
        """
        if price := child.get("data-preciomin", None):
            return float(price)
        return None
