import uuid
from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=False)
class Product:
    class Type(Enum):
        BASIC = "Basic"
        PREMIUM = "Premium"
        GOLD = "Gold"

    name: str
    description: str
    type: "Type"
    id: uuid.UUID = field(default_factory=uuid.uuid4)

