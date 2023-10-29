import re

from bs4 import BeautifulSoup, Tag

from brickpioneer import models
from brickpioneer.scrapers.base import BaseScraper


class NeinorHomes(BaseScraper):
    """
    Scraper class for fetching promotions from the Neinor Homes website.
    Example: https://www.neinorhomes.com/promociones/valencia
    """

    base_url: str = "https://www.neinorhomes.com/"

    @property
    def promotions_url(self) -> str:
        return f"{self.base_url}/promociones/{self.province}/"

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        return soup.find("section", class_="box-listado-promocion")

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        return parent.find_all("div", class_="box-vivienda", recursive=False)

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Extracts the promotion details from the given HTML element.
        """
        name_tag = child.find("h2")
        city = name_tag.span.text if name_tag.span else None
        name_tag.span.extract()
        link_tag = child.find("a", class_="btn btn-informacion")
        promotion = {
            "developer": self.__class__.__name__,
            "province": self.province_display,
            "city": city.strip() if city else None,
            "name": name_tag.get_text().strip() if name_tag else None,
            "price_min": self._get_promotion_price(child),
            "url": link_tag.get("href") if link_tag else None,
        }
        return models.Promotion(**promotion)

    def _get_promotion_price(self, child: Tag) -> float | None:
        """
        Extracts and parse the price from the given HTML element.
        """
        if price_tag := child.find("strong"):
            price_digits = "".join(re.findall(r"[\d]", price_tag.text or ""))
            return float(price_digits) if price_digits else None
        return None
