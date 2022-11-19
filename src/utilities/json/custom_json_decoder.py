import json
from datetime import datetime
from decimal import Decimal

from src.models.model import Product


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "datatype" in obj:
            if obj["datatype"] == "Decimal":
                return Decimal(obj["number"])
            elif obj["datatype"] == "Product":
                name = obj["name"]
                cost = obj["cost"]
                product = Product(name, cost)
                product._date_created = datetime.fromisoformat(obj["date_created"])
                return product
        return obj
