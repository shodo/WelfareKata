from datetime import datetime
import uuid
from dataclasses import dataclass
from welfarekata.webapp.models.purchase import Purchase


@dataclass(frozen=True)
class PurchaseDto:
    id: uuid.UUID
    account_id: uuid.UUID
    product_id: uuid.UUID
    credits: int
    creation_date: datetime

    @classmethod
    def from_orm(cls, purchase: Purchase) -> "PurchaseDto":
        return PurchaseDto(id=purchase.external_id,
                           account_id=purchase.account.external_id,
                           product_id=purchase.product.external_id,
                           credits=purchase.spent_credits,
                           creation_date=purchase.creation_date)
