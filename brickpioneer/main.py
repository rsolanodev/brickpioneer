from typing import Type

from brickpioneer import constants, helpers, models, scrapers


SCRAPER_CLASSES: list[Type[scrapers.BaseScraper]] = [
    scrapers.AedasHomes,
    scrapers.Habitat,
    scrapers.Metrovacesa,
    scrapers.NeinorHomes,
    scrapers.ViaCelere,
]


def fetch_properties(province: str = constants.VALENCIA) -> None:
    developers: list[scrapers.BaseScraper] = [
        scraper(province=province) for scraper in SCRAPER_CLASSES
    ]
    promotions: list[models.Promotion] = []
    for developer in developers:
        promotions.extend(developer.get_promotions())
    filename: str = helpers.promotions_to_csv(promotions)
    print(
        f"The CSV has been generated with {len(promotions)} promotions in: {filename}"
    )


if __name__ == "__main__":
    fetch_properties()
