from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class RawOffer:
    name: str
    measure_unit: str
    price_with_vat: Decimal
    price_without_vat: Decimal
    delivery_cost: Decimal
    extraction_date: datetime
    page_url: str
    image_url: str
