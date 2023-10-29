import attrs


@attrs.define
class Promotion:
    developer: str = attrs.field()
    province: str = attrs.field()
    city: str = attrs.field()
    name: str = attrs.field()
    url: str = attrs.field()
    price_min: str = attrs.field()
    is_available: bool = True
