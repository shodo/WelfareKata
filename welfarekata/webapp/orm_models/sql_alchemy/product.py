import enum
import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from welfarekata.webapp.orm_models.sql_alchemy.base import Base


class Product(Base):
    __tablename__ = 'webapp_product'

    class Type(enum.Enum):
        BASIC = "Basic"
        PREMIUM = "Premium"
        GOLD = "Gold"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), default=None, nullable=False)
    description = Column(String(400), default=None, nullable=False)
    type = Column(String(10), default=Type.BASIC.value, nullable=False)
