import re

from bs4 import BeautifulSoup, Tag

from brickpioneer import constants, models
from brickpioneer.scrapers.base import BaseScraper


class ViaCelere(BaseScraper):
    """
    Scraper class for fetching promotions from the Vía Célere website.
    Example: https://www.viacelere.com/en/projects?country=ES&provincia=Valencia
    """

    base_url: str = "https://www.viacelere.com"

    @property
    def promotions_url(self) -> str:
        return (
            f"{self.base_url}/promociones?country=ES&provincia={self.get_province_id()}"
        )

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        return soup.find("div", class_="mod__fichas-promociones")

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        return parent.find_all("div", class_="card", recursive=False)

    def get_province_id(self) -> str | None:
        """
        Retrieves the province ID of the website.
        """
        return {constants.VALENCIA: "Valencia"}.get(self.province, None)

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Extracts the promotion details from the given HTML element.
        """
        name_tag = child.find("h3")
        name_tag.span.extract()
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
        address = child.find("p", class_="article-summary article-summary--place")
        return address.text.split(",")[-1].strip()

    def _get_promotion_price(self, child: Tag) -> float | None:
        """
        Extracts and parse the price from the given HTML element.
        """
        if price_tag := child.find("strong", class_="text__promociones__money"):
            if "100% vendida" not in price_tag.text:
                price_digits = "".join(re.findall(r"[\d]", price_tag.text or ""))
                return float(price_digits) if price_digits else None
        return None

    def _validate_promotion(self, child: Tag) -> bool:
        """
        Validates if the promotion is still available.
        """
        return "100% vendida" not in child.text
