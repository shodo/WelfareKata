from datetime import datetime
from math import prod
from welfarekata.webapp.models.product import Product


class PricingService:
    pricing_registry = {
        Product.Type.BASIC: 100,
        Product.Type.PREMIUM: 200,
        Product.Type.GOLD: 300
    }

    @classmethod
    def calculate_price(
        cls,
        product_type: Product.Type,
        account_activation_date: datetime,
    ) -> int:
        price = cls.pricing_registry[product_type]

        if (datetime.now() - account_activation_date).days > 365:
            price = 300 * 0.1

        return int(price)