import uuid
from typing import Optional, List
from welfarekata.webapp.domain.exceptions import AccountAlreadyActivatedException
from welfarekata.webapp.dtos.account_dto import AccountDto
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
    def activate_account(cls, employee_id: uuid.UUID,) -> AccountDto:
        accounts_with_same_employee_count = Account.objects.filter(employee_external_id=employee_id).count()

        if accounts_with_same_employee_count > 0:
            raise AccountAlreadyActivatedException()

        account = Account(external_id=uuid.uuid4(), employee_external_id=employee_id, credits=cls.STARTING_CREDITS)
        account.save()

        return AccountDto.from_orm(account)
