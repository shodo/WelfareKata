from dataclasses import dataclass
from datetime import date
import uuid

from welfarekata.webapp.domain import Account


@dataclass(frozen=True)
class AccountDto:
    id: uuid.UUID
    employee_id: uuid.UUID
    activation_date: date
    credits: int

    @classmethod
    def from_entity(cls, account: Account) -> "AccountDto":
        return AccountDto(
            id=account.id,
            credits=account.credits,
            employee_id=account.employee_id,
            activation_date=account.activation_date,
        )
