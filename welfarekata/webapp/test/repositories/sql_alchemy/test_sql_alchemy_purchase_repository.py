import uuid
from datetime import date, datetime
from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_purchase_repository import SqlAlchemyPurchaseRepository
from welfarekata.webapp.test.sql_alchemy_test_case import SqlAlchemyTestCase
from welfarekata.webapp import domain
from welfarekata.webapp.orm_models import sql_alchemy as sqla_models


class TestSqlAlchemyPurchaseRepository(SqlAlchemyTestCase):
    def setUp(self):
        super(TestSqlAlchemyPurchaseRepository, self).setUp()

        self.orm_account = sqla_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )

        self.orm_product = sqla_models.Product(
            name="name",
            description="description",
            type=sqla_models.Product.Type.BASIC.value
        )

        session = self.session_factory(expire_on_commit=False)
        session.add(self.orm_account)
        session.add(self.orm_product)
        session.commit()

    def test_add(self):
        # Setup
        purchase = domain.Purchase(
            account_id=self.orm_account.external_id,
            product_id=self.orm_product.external_id,
            credits=100,
            creation_date=datetime.now()
        )

        session = self.session_factory()

        # SUT
        added_purchase = SqlAlchemyPurchaseRepository(session).add(purchase)
        session.commit()

        orm_added_purchase = session.query(sqla_models.Purchase).one()

        # Asserts
        self.assertEqual(orm_added_purchase.external_id, added_purchase.id)
        self.assertEqual(orm_added_purchase.account.external_id, added_purchase.account_id)
        self.assertEqual(orm_added_purchase.product.external_id, added_purchase.product_id)
        self.assertEqual(orm_added_purchase.spent_credits, added_purchase.credits)
        self.assertEqual(orm_added_purchase.creation_date, added_purchase.creation_date)

    def test_get(self):
        # Setup
        session = self.session_factory()

        orm_purchase = sqla_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=100,
        )
        session.add(orm_purchase)
        session.commit()

        # SUT
        retrieved_purchase = SqlAlchemyPurchaseRepository(session).get(orm_purchase.external_id)

        # Asserts
        self.assertEqual(orm_purchase.external_id, retrieved_purchase.id)
        self.assertEqual(orm_purchase.account.external_id, retrieved_purchase.account_id)
        self.assertEqual(orm_purchase.product.external_id, retrieved_purchase.product_id)
        self.assertEqual(orm_purchase.spent_credits, retrieved_purchase.credits)
        self.assertEqual(orm_purchase.creation_date, retrieved_purchase.creation_date)

    def test_list(self):
        # Setup
        session = self.session_factory()

        orm_purchase_one = sqla_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=100,
        )

        orm_purchase_two = sqla_models.Purchase(
            account_id=self.orm_account.id,
            product_id=self.orm_product.id,
            spent_credits=200,
        )

        session.add(orm_purchase_one)
        session.add(orm_purchase_two)
        session.commit()

        # SUT
        retrieved_purchases = SqlAlchemyPurchaseRepository(session).list()

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
