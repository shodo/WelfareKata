import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseDto:
    id: uuid.UUID
    account_id: uuid.UUID
    product_id: uuid.UUID
    credits: int
