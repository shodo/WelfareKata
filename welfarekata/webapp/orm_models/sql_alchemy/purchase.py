import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from welfarekata.webapp.orm_models.sql_alchemy.base import Base


class Purchase(Base):
    __tablename__ = 'webapp_purchase'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    spent_credits = Column(Integer, nullable=False, default=0)
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    account_id = Column(Integer, ForeignKey("webapp_account.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("webapp_product.id", ondelete="RESTRICT"), primary_key=True)

    account = relationship("Account")
    product = relationship("Product")
