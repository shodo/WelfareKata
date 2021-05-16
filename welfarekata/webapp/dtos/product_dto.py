import uuid
from dataclasses import dataclass
from enum import Enum

from welfarekata.webapp.domain import Product


@dataclass(frozen=True)
class ProductDto:
    class Type(Enum):
        BASIC = "Basic"
        PREMIUM = "Premium"
        GOLD = "Gold"

    id: uuid.UUID
    name: str
    description: str
    type: "Type"

    @classmethod
    def from_entity(cls, product: Product) -> "ProductDto":
        return ProductDto(
            id=product.id,
            name=product.name,
            description=product.description,
            type=ProductDto.Type(product.type.value)
        )
