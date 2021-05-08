from dataclasses import dataclass
from datetime import date
import uuid
from welfarekata.webapp.models.account import Account


@dataclass(frozen=True)
class AccountDto:
    id: uuid.UUID
    employee_id: uuid.UUID
    activation_date: date
    credits: int

    @classmethod
    def from_orm(cls, account: Account) -> "AccountDto":
        return AccountDto(
            id=account.external_id,
            credits=account.credits,
            employee_id=account.employee_external_id,
            activation_date=account.creation_date,
        )
