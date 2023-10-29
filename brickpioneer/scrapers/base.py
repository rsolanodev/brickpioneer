import abc
import logging
from typing import Any

import attrs
import requests
from bs4 import BeautifulSoup, Tag

from brickpioneer import constants, models


logger = logging.getLogger(__name__)


@attrs.define
class BaseScraper:
    """
    Base class for scraping content related to a specific province.
    """

    province: str
    province_display: str

    @property
    @abc.abstractmethod
    def promotions_url(self) -> str:
        """
        The URL to fetch the promotions. This must be implemented by child classes.
        """
        raise NotImplementedError

    @province.validator
    def validate_province(self, _: Any, value: str) -> None:
        """
        Validate if the provided province is one of the accepted codes.
        """
        if value not in constants.PROVINCE_CODES:
            raise ValueError(
                f"The value '{value}' for 'province' is not valid."
                f" Expected one of {', '.join(constants.PROVINCE_CODES)}."
            )

    @province_display.default
    def set_province_display(self) -> str | None:
        """
        Sets the display name for the province.
        """
        provinces = dict(constants.PROVINCES)
        return provinces.get(self.province, None)

    def get(self, url: str) -> bytes | None:
        """
        Fetch the content from the provided URL.
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.content
            logger.error(
                f"Request to {url} returned status code {response.status_code}."
            )
            return None
        except (requests.Timeout, requests.RequestException) as e:
            logger.exception(f"Error fetching {url}: {e}")
            return None

    def get_promotions(self) -> list[models.Promotion]:
        """
        Fetch and parse the promotions from the base URL.
        """
        if content := self.get(self.promotions_url):
            soup = BeautifulSoup(content, "html.parser")
            parent = self.get_parent_tag(soup)
            return [
                self.extract_promotion(child) for child in self.get_child_tags(parent)
            ]
        return []

    def get_parent_tag(self, soup: BeautifulSoup) -> Tag:
        """
        Abstract method to get the parent tag from the parsed HTML content.
        """
        raise NotImplementedError

    def get_child_tags(self, parent: Tag) -> list[Tag]:
        """
        Abstract method to retrieve child tags (promotions) from the parent tag.
        """
        raise NotImplementedError

    def extract_promotion(self, child: Tag) -> models.Promotion:
        """
        Abstract method to extract the promotion details from the child tag.
        """
        raise NotImplementedError
