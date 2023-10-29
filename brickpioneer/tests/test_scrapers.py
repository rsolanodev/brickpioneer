import pytest

from brickpioneer import constants, models, scrapers


DOMAIN = "https://rsolano.dev"
PROPERTY_NAME = "Ruben's House"
PROPERTY_PRICE = "45000"
PROPERTY_CITY = "Valencia"
PROPERTY_SHORT_URL = "/promociones/ruben-house/"
PROPERTY_URL = f"{DOMAIN}{PROPERTY_SHORT_URL}"

mocked_responses = {
    scrapers.ViaCelere: f"""
    <div class="mod__fichas-promociones">
        <div class="card">
            <a href="{ PROPERTY_SHORT_URL }">
                <h3 class="article-title article-title--promociones">
                    <span class="orange-t type-ws-r text__celere">Célere</span><br />{ PROPERTY_NAME }
                </h3>
                <p class="article-summary article-summary--place">
                    Spain , { PROPERTY_CITY }
                </p>
                <p class="article-summary article-summary--money">
                    From <br /><strong class="text__promociones__money">{ PROPERTY_PRICE } €</strong>
                </p>
            </a>
        </div>
    </div>
    """,
    scrapers.Metrovacesa: f"""
    <div class="row" id="cartas-promociones">
        <div
        data-preciomin="{ PROPERTY_PRICE }.00"
        data-provinciaName="Valencia"
        data-poblacionName="{ PROPERTY_CITY }"
        data-map-title="{PROPERTY_NAME}"
        >
            <div class="card-body pl-0 text-left">
                <a
                href="{ PROPERTY_URL }"
                class="btn btn-primary btn-outline-primary btn-development"
                ></a>
            </div>
        </div>
    </div>
    """,
    scrapers.Habitat: f"""
    <div id="list_promotions" class="row row-cols-1 row-cols-sm-3">
        <div class="col">
            <article class="card">
                <a href="{ PROPERTY_SHORT_URL }">
                    <div class="card-body">
                        <h3 class="card-title">{ PROPERTY_NAME }</h3>
                        <h4 class="card-localidad">
                            <i class="icon-geo"></i>{ PROPERTY_CITY }, Valencia
                        </h4>
                        <div class="precio_container">
                            <span>Desde</span>
                            <span class="precio">{ PROPERTY_PRICE } €</span>
                        </div>
                    </div>
                </a>
            </article>
        </div>
    </div>
    """,
    scrapers.NeinorHomes: f"""
    <section class="box-listado-promocion section-proximas-list">
        <div class="box-vivienda" data-code="9924">
            <div class="box-detalle-promo">
            <h2>{ PROPERTY_NAME } <span>{ PROPERTY_CITY }</span></h2>
            <div class="box-detalle-promo-text">
                <p>Desde <strong>{ PROPERTY_PRICE }</strong></p>
            </div>
            <div class="box-detalle-promo-boton">
                <a class="btn btn-informacion" href="{ PROPERTY_URL }">Más información</a>
            </div>
        </div>
    </section>
    """,
    scrapers.AedasHomes: f"""
    <div class="promo-wrapper cards-wrapper">
        <a class="card-promo card" href="{ PROPERTY_SHORT_URL }">
            <div class="promo-text">
                <span class="promo-title">{ PROPERTY_NAME }</span>
                <ul class="promo-description"><li>{ PROPERTY_CITY }</li></ul>
                <span class="promo-price">From { PROPERTY_PRICE } €</span>
            </div>
        </a>
    </div>
    """,
}


@pytest.fixture(params=mocked_responses.items())
def scraper(request, monkeypatch):
    scraper_class, mock_get_response = request.param

    def mock_get(self, url: str) -> str:
        return mock_get_response

    monkeypatch.setattr(scraper_class, "get", mock_get)
    monkeypatch.setattr(scraper_class, "base_url", DOMAIN)
    return scraper_class(province=constants.VALENCIA)


def test_get_promotions(scraper):
    promotions = scraper.get_promotions()
    for promotion in promotions:
        assert isinstance(promotion, models.Promotion)
        assert PROPERTY_NAME == promotion.name
        assert float(PROPERTY_PRICE) == promotion.price_min
        assert PROPERTY_CITY == promotion.city
        assert PROPERTY_URL == promotion.url
    assert len(promotions) == 1
