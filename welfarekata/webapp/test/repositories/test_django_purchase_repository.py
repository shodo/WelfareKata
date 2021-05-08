import uuid
from datetime import date, datetime

from dateutil.tz import UTC
from django.test import TestCase

from welfarekata.webapp.repositories.django_purchase_repository import DjangoPurchaseRepository
from welfarekata.webapp import domain
from welfarekata.webapp import models as django_models


class TestDjangoPurchaseRepository(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDjangoPurchaseRepository, cls).setUpClass()

        cls.orm_account = django_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )
        cls.orm_account.save()

        cls.orm_product = django_models.Product(
            name="name",
            description="description",
            type=django_models.Product.Type.BASIC.value
        )
        cls.orm_product.save()

    def test_add(self):
        # Setup
        purchase = domain.Purchase(
            account_id=self.orm_account.external_id,
            product_id=self.orm_product.external_id,
            credits=100,
            creation_date=datetime.now(tz=UTC)
        )

        # SUT
        added_purchase = DjangoPurchaseRepository().add(purchase)
        orm_added_purchase = django_models.Purchase.objects.all()[0]

        # Asserts
        self.assertEqual(orm_added_purchase.external_id, added_purchase.id)
        self.assertEqual(orm_added_purchase.account.external_id, added_purchase.account_id)
        self.assertEqual(orm_added_purchase.product.external_id, added_purchase.product_id)
        self.assertEqual(orm_added_purchase.spent_credits, added_purchase.credits)
        self.assertEqual(orm_added_purchase.creation_date, added_purchase.creation_date)

    def test_get(self):
        # Setup
        orm_purchase = django_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=100,
        )
        orm_purchase.save()

        # SUT
        retrieved_purchase = DjangoPurchaseRepository().get(orm_purchase.external_id)

        # Asserts
        self.assertEqual(orm_purchase.external_id, retrieved_purchase.id)
        self.assertEqual(orm_purchase.account.external_id, retrieved_purchase.account_id)
        self.assertEqual(orm_purchase.product.external_id, retrieved_purchase.product_id)
        self.assertEqual(orm_purchase.spent_credits, retrieved_purchase.credits)
        self.assertEqual(orm_purchase.creation_date, retrieved_purchase.creation_date)

    def test_list(self):
        # Setup
        orm_purchase_one = django_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=100,
        )
        orm_purchase_one.save()

        orm_purchase_two = django_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=200,
        )
        orm_purchase_two.save()

        # SUT
        retrieved_purchases = DjangoPurchaseRepository().list()

        # Asserts
        retrieved_purchase_one = next(iter([purchase for purchase in retrieved_purchases
                                            if purchase.id == orm_purchase_one.external_id]), None)
        self.assertEqual(orm_purchase_one.external_id, retrieved_purchase_one.id)
        self.assertEqual(orm_purchase_one.product.external_id, retrieved_purchase_one.product_id)
        self.assertEqual(orm_purchase_one.account.external_id, retrieved_purchase_one.account_id)
        self.assertEqual(orm_purchase_one.spent_credits, retrieved_purchase_one.credits)
        self.assertEqual(orm_purchase_one.creation_date, retrieved_purchase_one.creation_date)

        retrieved_purchase_two = next(iter([purchase for purchase in retrieved_purchases
                                            if purchase.id == orm_purchase_two.external_id]), None)
        self.assertEqual(orm_purchase_two.external_id, retrieved_purchase_two.id)
        self.assertEqual(orm_purchase_two.product.external_id, retrieved_purchase_two.product_id)
        self.assertEqual(orm_purchase_two.account.external_id, retrieved_purchase_two.account_id)
        self.assertEqual(orm_purchase_two.spent_credits, retrieved_purchase_two.credits)
        self.assertEqual(orm_purchase_two.creation_date, retrieved_purchase_two.creation_date)
