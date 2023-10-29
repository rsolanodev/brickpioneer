import attrs


@attrs.define
class Promotion:
    developer: str
    province: str
    city: str
    name: str
    url: str
    price_min: str
    is_available: bool = True
