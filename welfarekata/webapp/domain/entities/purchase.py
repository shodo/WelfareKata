from datetime import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Purchase:
    account_id: uuid.UUID
    product_id: uuid.UUID
    credits: int
    creation_date: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
