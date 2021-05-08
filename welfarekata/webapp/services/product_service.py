import uuid
from typing import Optional, List
from welfarekata.webapp.models.product import Product
from welfarekata.webapp.dtos.product_dto import ProductDto
from welfarekata.webapp.models import Account


class ProductService:
    @classmethod
    def get_product(cls, product_id: uuid.UUID) -> Optional[ProductDto]:
        try:
            product = Product.objects.get(external_id=product_id)
            return ProductDto.from_orm(product)
        except Account.DoesNotExist:
            return None

    @classmethod
    def list_products(cls) -> List[ProductDto]:
        products = Product.objects.all()
        return [ProductDto.from_orm(product) for product in products]

    @classmethod
    def create_product(cls, name: str, description: str, type: ProductDto.Type) -> ProductDto:
        product = Product(external_id=uuid.uuid4(), name=name, description=description, type=type.value)
        product.save()

        return ProductDto.from_orm(product)

    @classmethod
    def update_product(
        cls,
        product_id: uuid.UUID,
        name: str = None,
        description: str = None,
        type: ProductDto.Type = None,
    ) -> ProductDto:
        product = Product.objects.get(external_id=product_id)

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        if type is not None:
            product.type = type.value

        product.save()

        return ProductDto.from_orm(product)