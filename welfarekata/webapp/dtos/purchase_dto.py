from datetime import datetime
import uuid
from dataclasses import dataclass

from welfarekata.webapp.domain import Purchase


@dataclass(frozen=True)
class PurchaseDto:
    id: uuid.UUID
    account_id: uuid.UUID
    product_id: uuid.UUID
    credits: int
    creation_date: datetime

    @classmethod
    def from_entity(cls, purchase: Purchase) -> "PurchaseDto":
        return PurchaseDto(id=purchase.id,
                           account_id=purchase.account_id,
                           product_id=purchase.product_id,
                           credits=purchase.credits,
                           creation_date=purchase.creation_date)
