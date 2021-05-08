from dataclasses import dataclass
from datetime import date
import uuid


@dataclass(frozen=False)
class Account:
    employee_id: uuid.UUID
    activation_date: date
    credits: int
    id: uuid.UUID = uuid.uuid4()
