import uuid
from dataclasses import dataclass

from welfarekata.webapp.models import Account


@dataclass(frozen=True)
class AccountInfoDto:
    id: uuid.UUID
    credits: int

    @classmethod
    def from_orm(cls, account: Account) -> "AccountInfoDto":
        return AccountInfoDto(
            id=account.external_id,
            credits=account.credits,
        )
