from datetime import date

from welfarekata.webapp.domain import Product


class PricingService:
    pricing_registry = {
        Product.Type.BASIC: 100,
        Product.Type.PREMIUM: 200,
        Product.Type.GOLD: 300
    }

    @classmethod
    def calculate_price(cls, product_type: Product.Type, account_activation_date: date) -> int:
        price = cls.pricing_registry[product_type]

        if (date.today() - account_activation_date).days > 365:
            price = 300 * 0.1

        return int(price)