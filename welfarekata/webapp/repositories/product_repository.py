import uuid
from typing import Optional, List

from welfarekata.webapp import domain
from welfarekata.webapp import models as django_models
from welfarekata.webapp.domain.exceptions import ProductNotFoundException


class ProductRepository:
    @classmethod
    def get(cls, product_id: uuid.UUID) -> Optional[domain.Product]:
        try:
            django_product = django_models.Product.objects.get(external_id=product_id)
            return cls._from_django_product_to_domain_product(django_product)

        except django_models.Product.DoesNotExist:
            return None

    @classmethod
    def list(cls) -> List[domain.Product]:
        django_products = django_models.Product.objects.all()
        return [cls._from_django_product_to_domain_product(django_product) for django_product in django_products]

    @classmethod
    def add(cls, product: domain.Product) -> domain.Product:
        django_product = django_models.Product(
            external_id=product.id,
            name=product.name,
            description=product.description,
            type=django_models.Product.Type(product.type.value).value
        )
        django_product.save()

        return cls._from_django_product_to_domain_product(django_product)

    @classmethod
    def update(cls, product: domain.Product) -> domain.Product:
        try:
            django_product = django_models.Product.objects.get(external_id=product.id)
        except django_models.Product.DoesNotExist:
            raise ProductNotFoundException()

        django_product.name = product.name
        django_product.description = product.description
        django_product.type = django_models.Product.Type(product.type.value).value
        django_product.save()

        return cls._from_django_product_to_domain_product(django_product)

    @classmethod
    def _from_django_product_to_domain_product(cls, django_product: django_models.Product) -> domain.Product:
        return domain.Product(
            id=django_product.external_id,
            name=django_product.name,
            description=django_product.description,
            type=domain.Product.Type(django_product.type)
        )