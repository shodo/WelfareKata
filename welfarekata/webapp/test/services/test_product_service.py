from welfarekata.webapp.repositories.django_unit_of_work import DjangoUnitOfWork
from welfarekata.webapp.dtos import ProductDto
from welfarekata.webapp.models.product import Product
from welfarekata.webapp.domain.services import ProductService
from django.test import TestCase


class TestProductService(TestCase):
    def test_create_product(self):
        created_product_dto = ProductService(DjangoUnitOfWork()).create_product(
            name="Name",
            description="Descripton",
            type=ProductDto.Type.BASIC
        )

        products_on_db = Product.objects.all()
        self.assertEqual(len(products_on_db), 1)

        created_product_on_db = products_on_db[0]
        self.assertIsNotNone(created_product_dto)
        self.assertEqual(created_product_dto.id,
                         created_product_on_db.external_id)
        self.assertEqual(created_product_dto.name, created_product_on_db.name)
        self.assertEqual(created_product_dto.description,
                         created_product_on_db.description)
        self.assertEqual(created_product_dto.type.value,
                         created_product_on_db.type)

    def test_get_product(self):
        # Setup
        product = Product(name="Product",
                          description="Description",
                          type=Product.Type.BASIC.value)
        product.save()

        product_dto = ProductService(DjangoUnitOfWork()).get_product(product_id=product.external_id)

        self.assertIsNotNone(product_dto)
        self.assertEqual(product_dto.id, product.external_id)
        self.assertEqual(product_dto.description, product.description)
        self.assertEqual(product_dto.name, product.name)
        self.assertEqual(product_dto.type.value, product.type)

    def test_list_products(self):
        # Setup
        product_one = Product(name="Product1",
                              description="Description1",
                              type=Product.Type.BASIC.value)
        product_one.save()

        product_two = Product(name="Product2",
                              description="Description2",
                              type=Product.Type.GOLD.value)
        product_two.save()

        product_dtos = ProductService(DjangoUnitOfWork()).list_products()

        self.assertIsNotNone(product_dtos)
        self.assertEqual(len(product_dtos), 2)

        retrieved_one = next(
            (it for it in product_dtos if it.id == product_one.external_id),
            None)
        self.assertIsNotNone(retrieved_one)

        retrieved_two = next(
            (it for it in product_dtos if it.id == product_two.external_id),
            None)
        self.assertIsNotNone(retrieved_two)

    def test_update_product(self):
        # Setup
        product = Product(name="Product",
                          description="Description",
                          type=Product.Type.BASIC.value)
        product.save()

        product_dto = ProductService(DjangoUnitOfWork()).update_product(
            product_id=product.external_id,
            name="Updated Product",
            description="Updated Description",
            type=ProductDto.Type.PREMIUM
        )

        self.assertIsNotNone(product_dto)
        self.assertEqual(product_dto.id, product.external_id)
        self.assertEqual(product_dto.description, "Updated Description")
        self.assertEqual(product_dto.name, "Updated Product")
        self.assertEqual(product_dto.type, ProductDto.Type.PREMIUM)
