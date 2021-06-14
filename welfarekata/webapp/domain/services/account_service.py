import uuid
from datetime import date
from typing import Optional, List

from welfarekata.webapp.domain import UnitOfWork
from welfarekata.webapp.domain import Account
from welfarekata.webapp.domain.exceptions import AccountAlreadyActivatedException
from welfarekata.webapp.dtos.account_dto import AccountDto


class AccountService:
    STARTING_CREDITS = 1000

    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work

    def get_account(self, account_id: uuid.UUID) -> Optional[AccountDto]:
        account = self.uow.account_repository.get(account_id)
        return AccountDto.from_entity(account) if account else None

    def list_accounts(self) -> List[AccountDto]:
        accounts = self.uow.account_repository.list()
        return [AccountDto.from_entity(account) for account in accounts]

    def activate_account(self, employee_id: uuid.UUID) -> AccountDto:
        accounts_with_same_employee_count = len(self.uow.account_repository.list(employee_id))

        if accounts_with_same_employee_count > 0:
            raise AccountAlreadyActivatedException()

        account = Account(employee_id=employee_id, activation_date=date.today(), credits=self.STARTING_CREDITS)
        self.uow.account_repository.add(account)

        return AccountDto.from_entity(account)