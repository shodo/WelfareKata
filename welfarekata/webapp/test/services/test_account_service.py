from datetime import datetime
import uuid
from venv import create
from welfarekata.webapp.services import AccountService
from welfarekata.webapp.models.account import Account
from django.test import TestCase


class TestAccountService(TestCase):
    def test_create_account(self):
        # Setup
        employee_id = uuid.uuid4()
        created_account_dto = AccountService.create_account(employee_id)

        accounts_on_db = Account.objects.all()
        self.assertEqual(len(accounts_on_db), 1)

        created_account_from_db = accounts_on_db[0]
        self.assertIsNotNone(created_account_dto)
        self.assertEqual(created_account_dto.id,
                         created_account_from_db.external_id)
        self.assertEqual(created_account_dto.employee_id,
                         created_account_from_db.employee_external_id)
        self.assertEqual(created_account_dto.activation_date,
                         created_account_from_db.creation_date)
        self.assertEqual(created_account_dto.credits,
                         created_account_from_db.credits)

    def test_get_account(self):
        # Setup
        account = Account(credits=200,
                          employee_external_id=uuid.uuid4(),
                          creation_date=datetime(2015, 1, 1))
        account.save()

        account_dto = AccountService.get_account(
            account_id=account.external_id)

        self.assertIsNotNone(account_dto)
        self.assertEqual(account_dto.id, account.external_id)
        self.assertEqual(account_dto.employee_id, account.employee_external_id)
        self.assertEqual(account_dto.activation_date, account.creation_date)
        self.assertEqual(account_dto.credits, account.credits)

    def test_list_accounts(self):
        # Setup
        account_one = Account(credits=200,
                              employee_external_id=uuid.uuid4(),
                              creation_date=datetime(2015, 1, 1))
        account_one.save()

        account_two = Account(credits=200,
                              employee_external_id=uuid.uuid4(),
                              creation_date=datetime(2015, 1, 1))
        account_two.save()

        account_dtos = AccountService.list_accounts()

        self.assertIsNotNone(account_dtos)
        self.assertEqual(len(account_dtos), 2)

        retrieved_one = next(
            (it for it in account_dtos if it.id == account_one.external_id),
            None)
        self.assertIsNotNone(retrieved_one)

        retrieved_two = next(
            (it for it in account_dtos if it.id == account_two.external_id),
            None)
        self.assertIsNotNone(retrieved_two)
