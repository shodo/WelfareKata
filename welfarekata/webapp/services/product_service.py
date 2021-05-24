import uuid
from typing import Optional, List

from welfarekata.webapp.domain import UnitOfWork
from welfarekata.webapp.domain import Product
from welfarekata.webapp.dtos.product_dto import ProductDto


class ProductService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work

    def get_product(self, product_id: uuid.UUID) -> Optional[ProductDto]:
        product = self.uow.product_repository.get(product_id)
        return ProductDto.from_entity(product) if product else None

    def list_products(self) -> List[ProductDto]:
        products = self.uow.product_repository.list()
        return [ProductDto.from_entity(product) for product in products]

    def create_product(self, name: str, description: str, type: ProductDto.Type) -> ProductDto:
        product = Product(name=name, description=description, type=Product.Type(type.value))
        self.uow.product_repository.add(product)

        return ProductDto.from_entity(product)

    def update_product(
        self,
        product_id: uuid.UUID,
        name: str = None,
        description: str = None,
        type: ProductDto.Type = None,
    ) -> ProductDto:
        product = self.uow.product_repository.get(product_id)

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        if type is not None:
            product.type = Product.Type(type.value)

        updated_product = self.uow.product_repository.update(product)

        return ProductDto.from_entity(updated_product)
