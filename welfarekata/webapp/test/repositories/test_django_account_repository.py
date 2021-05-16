import uuid
from datetime import date

from django.test import TestCase

from welfarekata.webapp.repositories.django_account_repository import DjangoAccountRepository
from welfarekata.webapp import domain
from welfarekata.webapp import models as django_models


class TestDjangoAccountRepository(TestCase):
    def test_add(self):
        # Setup
        account = domain.Account(
            employee_id=uuid.uuid4(),
            activation_date=date.today(),
            credits=100,
        )

        # SUT
        added_account = DjangoAccountRepository().add(account)
        orm_added_account = django_models.Account.objects.all()[0]

        # Asserts
        self.assertEqual(added_account, account)
        self.assertEqual(orm_added_account.external_id, added_account.id)
        self.assertEqual(orm_added_account.employee_external_id, added_account.employee_id)
        self.assertEqual(orm_added_account.credits, added_account.credits)
        self.assertEqual(orm_added_account.creation_date, added_account.activation_date)

    def test_get(self):
        # Setup
        orm_account = django_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )
        orm_account.save()

        # SUT
        retrieved_account = DjangoAccountRepository().get(orm_account.external_id)
        retrieved_account_for_update = DjangoAccountRepository().get(orm_account.external_id, for_update=True)

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
        orm_account_one = django_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )
        orm_account_one.save()

        orm_account_two = django_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=200,
        )
        orm_account_two.save()

        # SUT
        retrieved_accounts = DjangoAccountRepository().list()

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
        orm_account = django_models.Account(
            employee_external_id=uuid.uuid4(),
            creation_date=date.today(),
            credits=100,
        )
        orm_account.save()

        # SUT
        new_account = domain.Account(
            id=orm_account.external_id,
            employee_id=uuid.uuid4(),
            activation_date=date.today(),
            credits=50,
        )
        orm_account.save()

        updated_account = DjangoAccountRepository().update(new_account)
        updated_orm_account = django_models.Account.objects.get(id=orm_account.id)

        # Asserts
        self.assertEqual(updated_account.id, new_account.id)
        self.assertEqual(updated_account.credits, new_account.credits)
        self.assertEqual(updated_account.employee_id, new_account.employee_id)
        self.assertEqual(updated_account.activation_date, new_account.activation_date)

        self.assertEqual(updated_orm_account.external_id, updated_account.id)
        self.assertEqual(updated_orm_account.employee_external_id, updated_account.employee_id)
        self.assertEqual(updated_orm_account.credits, updated_account.credits)
        self.assertEqual(updated_orm_account.creation_date, updated_account.activation_date)