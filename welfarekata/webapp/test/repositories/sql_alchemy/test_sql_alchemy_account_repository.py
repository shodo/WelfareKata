import uuid
from datetime import date

from welfarekata.webapp.repositories.sql_alchemy.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from welfarekata.webapp.test.sql_alchemy_test_case import SqlAlchemyTestCase
from welfarekata.webapp import domain
import welfarekata.webapp.orm_models.sql_alchemy as sqla_models


class TestSqlAlchemyAccountRepository(SqlAlchemyTestCase):
    def test_add(self):
        # Setup
        account = domain.Account(
            employee_id=uuid.uuid4(),
            activation_date=date.today(),
            credits=100,
        )

        # SUT
        session = self.session_factory()
        added_account = SqlAlchemyAccountRepository(session).add(account)
        session.commit()

        orm_added_account = session.query(sqla_models.Account).one()

        # Asserts
        self.assertEqual(added_account, account)
        self.assertEqual(orm_added_account.external_id, added_account.id)
        self.assertEqual(orm_added_account.employee_external_id, added_account.employee_id)
        self.assertEqual(orm_added_account.credits, added_account.credits)
        self.assertEqual(orm_added_account.creation_date, added_account.activation_date)

    def test_get(self):
        # Setup
        self.session = self.session_factory()
        orm_account = sqla_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )
        self.session.add(orm_account)
        self.session.commit()

        # SUT
        retrieved_account = SqlAlchemyAccountRepository(self.session).get(orm_account.external_id)
        retrieved_account_for_update = SqlAlchemyAccountRepository(self.session).get(
            orm_account.external_id,
            for_update=True
        )

        # Asserts
        self.assertEqual(orm_account.external_id, retrieved_account.id)
        self.assertEqual(orm_account.employee_external_id, retrieved_account.employee_id)
        self.assertEqual(orm_account.credits, retrieved_account.credits)
        self.assertEqual(orm_account.creation_date, retrieved_account.activation_date)

        self.assertEqual(orm_account.external_id, retrieved_account_for_update.id)
        self.assertEqual(orm_account.employee_external_id, retrieved_account_for_update.employee_id)
        self.assertEqual(orm_account.credits, retrieved_account_for_update.credits)
        self.assertEqual(orm_account.creation_date, retrieved_account_for_update.activation_date)

    def test_list(self):
        # Setup
        self.session = self.session_factory()
        orm_account_one = sqla_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )

        orm_account_two = sqla_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=200,
        )

        self.session.add(orm_account_one)
        self.session.add(orm_account_two)
        self.session.commit()

        # SUT
        retrieved_accounts = SqlAlchemyAccountRepository(self.session).list()

        # Asserts
        retrieved_account_one = next(iter([account for account in retrieved_accounts
                                           if account.id == orm_account_one.external_id]), None)
        self.assertEqual(orm_account_one.external_id, retrieved_account_one.id)
        self.assertEqual(orm_account_one.employee_external_id, retrieved_account_one.employee_id)
        self.assertEqual(orm_account_one.credits, retrieved_account_one.credits)
        self.assertEqual(orm_account_one.creation_date, retrieved_account_one.activation_date)

        retrieved_account_two = next(iter([account for account in retrieved_accounts
                                           if account.id == orm_account_two.external_id]), None)
        self.assertEqual(orm_account_two.external_id, retrieved_account_two.id)
        self.assertEqual(orm_account_two.employee_external_id, retrieved_account_two.employee_id)
        self.assertEqual(orm_account_two.credits, retrieved_account_two.credits)
        self.assertEqual(orm_account_two.creation_date, retrieved_account_two.activation_date)

    def test_update(self):
        # Setup
        self.session = self.session_factory()

        orm_account = sqla_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )

        self.session.add(orm_account)
        self.session.commit()

        new_account = domain.Account(
            id=orm_account.external_id,
            employee_id=uuid.uuid4(),
            activation_date=date.today(),
            credits=50,
        )

        # SUT
        updated_account = SqlAlchemyAccountRepository(self.session).update(new_account)
        self.session.commit()

        updated_orm_account = self.session.query(sqla_models.Account).get(orm_account.id)

        # Asserts
        self.assertEqual(updated_account.id, new_account.id)
        self.assertEqual(updated_account.credits, new_account.credits)
        self.assertEqual(updated_account.employee_id, new_account.employee_id)
        self.assertEqual(updated_account.activation_date, new_account.activation_date)

        self.assertEqual(updated_orm_account.external_id, updated_account.id)
        self.assertEqual(updated_orm_account.employee_external_id, updated_account.employee_id)
        self.assertEqual(updated_orm_account.credits, updated_account.credits)
        self.assertEqual(updated_orm_account.creation_date, updated_account.activation_date)