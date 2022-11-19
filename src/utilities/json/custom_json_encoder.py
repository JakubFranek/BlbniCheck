import json
from datetime import datetime
from decimal import Decimal

from src.models.model import Product


class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(indent=2, separators=(", ", ": "))

    def default(self, arg):
        if isinstance(arg, datetime):
            return arg.isoformat()
        elif isinstance(arg, Product):
            return dict(
                datatype="Product",
                name=arg.name,
                cost=arg.cost,
                date_created=arg.date_created.isoformat(),
            )
        elif isinstance(arg, Decimal):
            return dict(datatype="Decimal", number=str(arg))
        else:
            super().default(arg)
