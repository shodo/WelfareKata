from datetime import datetime
from unittest import mock
import uuid
from dateutil.tz import UTC

from welfarekata.webapp.repositories.django_unit_of_work import DjangoUnitOfWork
from welfarekata.webapp.domain.exceptions import NoEnoughCreditsException
from welfarekata.webapp.domain.exceptions import ProductNotFoundException, AccountNotFoundException
from welfarekata.webapp.models.account import Account
from welfarekata.webapp.services import PurchaseService
from welfarekata.webapp.models.purchase import Purchase
from welfarekata.webapp.models.product import Product
from django.test import TestCase


class TestPurchaseService(TestCase):
    def test_create_when_given_product_not_found_raise_exception(self):
        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        with self.assertRaises(ProductNotFoundException):
            invalid_product_id = uuid.uuid4()
            PurchaseService(
                DjangoUnitOfWork()
            ).do_purchase(account_id=account.external_id, product_id=invalid_product_id)

    def test_create_when_given_account_not_found_raise_exception(self):
        product = Product(name="Product1",
                          description="Description1",
                          type=Product.Type.BASIC.value)
        product.save()

        with self.assertRaises(AccountNotFoundException):
            invalid_account_id = uuid.uuid4()
            PurchaseService(
                DjangoUnitOfWork()
            ).do_purchase(account_id=invalid_account_id, product_id=product.external_id)

    @mock.patch("welfarekata.webapp.services.purchase_service.PricingService")
    def test_create_when_price_greater_then_credits_raise_exception(
            self, pricing_service_mock):
        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        product = Product(name="Product1",
                          description="Description1",
                          type=Product.Type.BASIC.value)
        product.save()

        pricing_service_mock.calculate_price.return_value = 300

        with self.assertRaises(NoEnoughCreditsException):
            PurchaseService(
                DjangoUnitOfWork()
            ).do_purchase(account_id=account.external_id, product_id=product.external_id)

    @mock.patch("welfarekata.webapp.services.purchase_service.PricingService")
    def test_create_when_everything_is_valid(self, pricing_service_mock):
        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        product = Product(name="Product1",
                          description="Description1",
                          type=Product.Type.BASIC.value)
        product.save()

        pricing_service_mock.calculate_price.return_value = 100

        created_purchase_dto = PurchaseService(
            DjangoUnitOfWork()
        ).do_purchase(account_id=account.external_id, product_id=product.external_id)

        purchases_on_db = Purchase.objects.all()

        self.assertEqual(len(purchases_on_db), 1)
        purchases_on_db = purchases_on_db[0]

        self.assertIsNotNone(created_purchase_dto)
        self.assertEqual(created_purchase_dto.id, purchases_on_db.external_id)
        self.assertEqual(created_purchase_dto.account_id,
                         purchases_on_db.account.external_id)
        self.assertEqual(created_purchase_dto.product_id,
                         purchases_on_db.product.external_id)
        self.assertEqual(created_purchase_dto.credits,
                         purchases_on_db.spent_credits)
        self.assertEqual(created_purchase_dto.creation_date,
                         purchases_on_db.creation_date)

    def test_get_purchase(self):
        # Setup
        product = Product(name="Product1",
                          description="Description1",
                          type=Product.Type.BASIC.value)
        product.save()

        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        purchase = Purchase(product=product,
                            account=account,
                            spent_credits=100,
                            creation_date=datetime(2015, 1, 1, tzinfo=UTC))
        purchase.save()

        purchase_dto = PurchaseService(
            DjangoUnitOfWork()
        ).get_purchase(purchase_id=purchase.external_id)

        self.assertIsNotNone(purchase_dto)
        self.assertEqual(purchase_dto.id, purchase.external_id)
        self.assertEqual(purchase_dto.account_id, purchase.account.external_id)
        self.assertEqual(purchase_dto.product_id, purchase.product.external_id)
        self.assertEqual(purchase_dto.credits, purchase.spent_credits)
        self.assertEqual(purchase_dto.creation_date, purchase.creation_date)

    def test_list_purchases(self):
        # Setup
        product = Product(name="Product1",
                          description="Description1",
                          type=Product.Type.BASIC.value)
        product.save()

        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        purchase_one = Purchase(product=product,
                                account=account,
                                spent_credits=100,
                                creation_date=datetime(2015, 1, 1))
        purchase_one.save()

        purchase_two = Purchase(product=product,
                                account=account,
                                spent_credits=100,
                                creation_date=datetime(2015, 1, 1))
        purchase_two.save()

        purchase_dtos = PurchaseService(
            DjangoUnitOfWork()
        ).list_purchases()

        self.assertIsNotNone(purchase_dtos)
        self.assertEqual(len(purchase_dtos), 2)

        retrieved_one = next(
            (it for it in purchase_dtos if it.id == purchase_one.external_id),
            None)
        self.assertIsNotNone(retrieved_one)

        retrieved_two = next(
            (it for it in purchase_dtos if it.id == purchase_two.external_id),
            None)
        self.assertIsNotNone(retrieved_two)
