import csv
import datetime

from brickpioneer import models


def generate_filename() -> str:
    """
    This function will generate a unique filename based on the current timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"data/promotions_{timestamp}.csv"


def promotions_to_csv(promotions: list[models.Promotion]) -> str:
    """
    This function will convert a list of promotion objects to a CSV file.
    """
    filename: str = generate_filename()
    with open(filename, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Promotor",
                "Provincia",
                "Ciudad",
                "Nombre",
                "Precio Mínimo",
                "Disponibilidad",
                "Enlace",
            ]
        )
        for promotion in promotions:
            writer.writerow(
                [
                    promotion.developer,
                    promotion.province,
                    promotion.city,
                    promotion.name,
                    promotion.price_min,
                    promotion.is_available,
                    promotion.url,
                ]
            )
    return filename
