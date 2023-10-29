import re

from bs4 import BeautifulSoup, Tag

from brickpioneer import constants, models
from brickpioneer.scrapers.base import BaseScraper


class AedasHomes(BaseScraper):
    """
    Scraper class for fetching promotions from the Aedas Homes website.
    Example: https://www.aedashomes.com/en/new-homes?province=2509951
    """

    base_url: str = "https://www.aedashomes.com"

    @property
    def promotions_url(self) -> str:
        return f"{self.base_url}/en/new-homes?province={self.get_province_id()}"

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        return soup.find("div", class_="promo-wrapper cards-wrapper")

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        return parent.find_all("a", recursive=False)

    def get_province_id(self) -> str | None:
        """
        Retrieves the province ID of the website.
        """
        return {constants.VALENCIA: "2509951"}.get(self.province, None)

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Extracts the promotion details from the given HTML element.
        """
        name_tag = child.find("span", class_="promo-title")
        description_tag = child.find("ul", class_="promo-description")
        city_tag = description_tag.find("li")
        promotion = {
            "developer": self.__class__.__name__,
            "province": self.province_display,
            "city": city_tag.text.strip() if city_tag else None,
            "name": name_tag.text.strip() if name_tag else None,
            "price_min": self._get_promotion_price(child),
            "url": f"{self.base_url}{child.get('href')}",
            "is_available": self._validate_promotion(child),
        }
        return models.Promotion(**promotion)

    def _get_promotion_price(self, child: Tag) -> float | None:
        """
        Extracts the price from the given HTML element.
        """
        if price_tag := child.find("span", class_="promo-price"):
            price_digits = "".join(re.findall(r"[\d]", price_tag.text or ""))
            return float(price_digits) if price_digits else None
        return None

    def _validate_promotion(self, child: Tag) -> bool:
        """
        Validates if the promotion is still available.
        """
        return "Sold" not in child.text
