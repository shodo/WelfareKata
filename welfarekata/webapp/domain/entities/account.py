from dataclasses import dataclass, field
from datetime import date
import uuid


@dataclass(frozen=True)
class Account:
    employee_id: uuid.UUID
    activation_date: date
    credits: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)
