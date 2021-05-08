import uuid
from dataclasses import dataclass
from enum import Enum
from welfarekata.webapp.models.product import Product


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
    def from_orm(cls, product: Product) -> "ProductDto":
        return ProductDto(
            id=product.external_id,
            name=product.name,
            description=product.description,
            type=ProductDto.Type[product.type.value],
        )
