import uuid
from typing import Optional, List

from welfarekata.webapp.repositories.django_product_repository import DjangoProductRepository
from welfarekata.webapp.domain.entities.product import Product
from welfarekata.webapp.dtos.product_dto import ProductDto


class ProductService:
    @classmethod
    def get_product(cls, product_id: uuid.UUID) -> Optional[ProductDto]:
        product = DjangoProductRepository.get(product_id)
        return ProductDto.from_entity(product) if product else None

    @classmethod
    def list_products(cls) -> List[ProductDto]:
        products = DjangoProductRepository.list()
        return [ProductDto.from_entity(product) for product in products]

    @classmethod
    def create_product(cls, name: str, description: str, type: ProductDto.Type) -> ProductDto:
        product = Product(name=name, description=description, type=Product.Type(type.value))
        DjangoProductRepository.add(product)

        return ProductDto.from_entity(product)

    @classmethod
    def update_product(
        cls,
        product_id: uuid.UUID,
        name: str = None,
        description: str = None,
        type: ProductDto.Type = None,
    ) -> ProductDto:
        product = DjangoProductRepository.get(product_id)

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        if type is not None:
            product.type = Product.Type(type.value)

        updated_product = DjangoProductRepository.update(product)

        return ProductDto.from_entity(updated_product)
