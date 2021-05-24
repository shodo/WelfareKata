import uuid
from datetime import date

from sqlalchemy import Column, Integer, Date
from sqlalchemy.dialects.postgresql import UUID

from welfarekata.webapp.orm_models.sql_alchemy.base import Base


class Account(Base):
    __tablename__ = 'webapp_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    employee_external_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    credits = Column(Integer, nullable=False, default=0)
    creation_date = Column(Date, nullable=False, default=date.today)
