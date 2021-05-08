import uuid
from datetime import date
from typing import Optional, List

from webapp.repositories.django_account_repository import DjangoAccountRepository
from welfarekata.webapp.domain.exceptions import AccountAlreadyActivatedException
from welfarekata.webapp.dtos.account_dto import AccountDto
from welfarekata.webapp.domain.entities.account import Account


class AccountService:
    STARTING_CREDITS = 1000

    @classmethod
    def get_account(cls, account_id: uuid.UUID) -> Optional[AccountDto]:
        account = DjangoAccountRepository.get(account_id)
        return AccountDto.from_entity(account)

    @classmethod
    def list_accounts(cls) -> List[AccountDto]:
        accounts = DjangoAccountRepository.list()
        return [AccountDto.from_entity(account) for account in accounts]

    @classmethod
    def activate_account(cls, employee_id: uuid.UUID,) -> AccountDto:
        accounts_with_same_employee_count = len(DjangoAccountRepository.list(employee_id))

        if accounts_with_same_employee_count > 0:
            raise AccountAlreadyActivatedException()

        account = Account(employee_id=employee_id, activation_date=date.today(), credits=cls.STARTING_CREDITS)
        DjangoAccountRepository.add(account)

        return AccountDto.from_entity(account)
