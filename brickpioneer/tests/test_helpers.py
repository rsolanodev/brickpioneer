import csv
import os

from brickpioneer import helpers, models


def test_promotions_to_csv(monkeypatch):
    promotions = [
        models.Promotion(
            developer="Ruben's Homes",
            province="Valencia",
            city="Valencia",
            name="Hilltop",
            url="http://rsolano.dev/hilltop",
            price_min=1234,
            is_available=True,
        ),
        models.Promotion(
            developer="Ruben's Homes",
            province="Valencia",
            city="Valencia",
            name="Woodbury",
            url="http://rsolano.dev/woodbury",
            price_min=6789,
            is_available=True,
        ),
    ]
    filename = helpers.promotions_to_csv(promotions)
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        assert header == [
            "Promotor",
            "Provincia",
            "Ciudad",
            "Nombre",
            "Precio Mínimo",
            "Disponibilidad",
            "Enlace",
        ]
        for idx, row in enumerate(reader):
            promo = promotions[idx]
            assert row == [
                promo.developer,
                promo.province,
                promo.city,
                promo.name,
                str(promo.price_min),
                str(promo.is_available),
                promo.url,
            ]
    os.remove(filename)
