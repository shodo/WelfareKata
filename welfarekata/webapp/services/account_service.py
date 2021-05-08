import uuid
from datetime import date
from typing import Optional, List
from welfarekata.webapp.dtos.account_dto import AccountDto

from django.db import transaction

from welfarekata.webapp.models import Account


class AccountService:
    STARTING_CREDITS = 1000

    @classmethod
    def get_account(cls, account_id: uuid.UUID) -> Optional[AccountDto]:
        try:
            account = Account.objects.get(external_id=account_id)
            return AccountDto.from_orm(account)

        except Account.DoesNotExist:
            return None

    @classmethod
    def list_accounts(cls) -> List[AccountDto]:
        accounts = Account.objects.all()
        return [AccountDto.from_orm(account) for account in accounts]

    @classmethod
    def create_account(
        cls,
        employee_id: uuid.UUID,
    ) -> AccountDto:
        account = Account(external_id=uuid.uuid4(),
                          employee_id=employee_id,
                          credits=cls.STARTING_CREDITS)
        account.save()

        return AccountDto.from_orm(account)
