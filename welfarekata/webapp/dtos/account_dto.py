from dataclasses import dataclass
from datetime import date
from typing import List
import uuid
from welfarekata.webapp.models.account import Account

from welfarekata.webapp.dtos.account_info_dto import AccountInfoDto
from welfarekata.webapp.dtos.purchase_dto import PurchaseDto


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
