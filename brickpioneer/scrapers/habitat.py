import re

from bs4 import BeautifulSoup, Tag

from brickpioneer import models
from brickpioneer.scrapers.base import BaseScraper


class Habitat(BaseScraper):
    """
    Scraper class for fetching promotions from the Habitat Inmobiliaria website.
    Example: https://www.habitatinmobiliaria.com/promociones/valencia/
    """

    base_url: str = "https://www.habitatinmobiliaria.com"

    @property
    def promotions_url(self) -> str:
        return f"{self.base_url}/promociones/{self.province}"

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        return soup.find(id="list_promotions")

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        return parent.find_all("div", recursive=False)

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Extracts the promotion details from the given HTML element.
        """
        name_tag = child.find("h3")
        link_tag = child.find("a")
        promotion = {
            "developer": self.__class__.__name__,
            "province": self.province_display,
            "city": self._get_promotion_city(child),
            "name": name_tag.text.strip() if name_tag else None,
            "price_min": self._get_promotion_price(child),
            "url": f"{self.base_url}{link_tag.get('href')}",
            "is_available": self._validate_promotion(child),
        }
        return models.Promotion(**promotion)

    def _get_promotion_city(self, child: Tag) -> str:
        """
        Extracts the city from the given HTML element.
        """
        address_tag = child.find("h4")
        return address_tag.text.split(",")[0].strip()

    def _get_promotion_price(self, child: Tag) -> float | None:
        """
        Extracts and parse the price from the given HTML element.
        """
        if price_tag := child.find("span", class_="precio"):
            price_digits = "".join(re.findall(r"[\d]", price_tag.text or ""))
            return float(price_digits) if price_digits else None
        return None

    def _validate_promotion(self, child: Tag) -> bool:
        """
        Validates if the promotion is still available.
        """
        return "Promoción entregada" not in child.text
