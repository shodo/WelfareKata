from django.test import TestCase

from welfarekata.webapp.repositories.django_product_repository import DjangoProductRepository
from welfarekata.webapp import domain
from welfarekata.webapp import models as django_models


class TestDjangoProductRepository(TestCase):
    def test_add(self):
        # Setup
        product = domain.Product(
            name="name",
            description="description",
            type=domain.Product.Type.BASIC,
        )

        # SUT
        added_product = DjangoProductRepository().add(product)
        orm_added_product = django_models.Product.objects.all()[0]

        # Asserts
        self.assertEqual(added_product, product)
        self.assertEqual(orm_added_product.external_id, added_product.id)
        self.assertEqual(orm_added_product.name, added_product.name)
        self.assertEqual(orm_added_product.description, added_product.description)
        self.assertEqual(orm_added_product.type, django_models.Product.Type(added_product.type.value).value)

    def test_get(self):
        # Setup
        orm_product = django_models.Product(
            name="name",
            description="description",
            type=django_models.Product.Type.BASIC.value
        )
        orm_product.save()

        # SUT
        retrieved_product = DjangoProductRepository().get(orm_product.external_id)

        # Asserts
        self.assertEqual(orm_product.external_id, retrieved_product.id)
        self.assertEqual(orm_product.name, retrieved_product.name)
        self.assertEqual(orm_product.description, retrieved_product.description)
        self.assertEqual(orm_product.type, django_models.Product.Type(retrieved_product.type.value).value)

    def test_list(self):
        # Setup
        orm_product_one = django_models.Product(
            name="name1",
            description="description1",
            type=django_models.Product.Type.BASIC.value
        )
        orm_product_one.save()

        orm_product_two = django_models.Product(
            name="name2",
            description="description2",
            type=django_models.Product.Type.GOLD.value
        )
        orm_product_two.save()

        # SUT
        retrieved_products = DjangoProductRepository().list()

        # Asserts
        retrieved_product_one = next(iter([product for product in retrieved_products
                                           if product.id == orm_product_one.external_id]), None)
        self.assertEqual(orm_product_one.external_id, retrieved_product_one.id)
        self.assertEqual(orm_product_one.name, retrieved_product_one.name)
        self.assertEqual(orm_product_one.description, retrieved_product_one.description)
        self.assertEqual(orm_product_one.type, django_models.Product.Type(retrieved_product_one.type.value).value)

        retrieved_product_two = next(iter([product for product in retrieved_products
                                           if product.id == orm_product_two.external_id]), None)
        self.assertEqual(orm_product_two.external_id, retrieved_product_two.id)
        self.assertEqual(orm_product_two.name, retrieved_product_two.name)
        self.assertEqual(orm_product_two.description, retrieved_product_two.description)
        self.assertEqual(orm_product_two.type, django_models.Product.Type(retrieved_product_two.type.value).value)

    def test_update(self):
        # Setup
        orm_product = django_models.Product(
            name="name1",
            description="description1",
            type=django_models.Product.Type.BASIC.value
        )
        orm_product.save()

        # SUT
        new_product = domain.Product(
            id=orm_product.external_id,
            name="updated_name",
            description="updated_description",
            type=domain.Product.Type.GOLD
        )
        updated_product = DjangoProductRepository().update(new_product)
        updated_orm_product = django_models.Product.objects.get(id=orm_product.id)

        # Asserts
        self.assertEqual(updated_product.id, new_product.id)
        self.assertEqual(updated_product.name, new_product.name)
        self.assertEqual(updated_product.description, new_product.description)
        self.assertEqual(updated_product.type, new_product.type)

        self.assertEqual(updated_orm_product.external_id, updated_product.id)
        self.assertEqual(updated_orm_product.name, updated_product.name)
        self.assertEqual(updated_orm_product.description, updated_product.description)
        self.assertEqual(updated_orm_product.type, django_models.Product.Type(updated_product.type.value).value)