import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Statements(Base):
    __tablename__ = "statements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False)
    interest_date = Column(DateTime, nullable=False)
    amount = Column(Integer, nullable=False)
    account = Column(String, nullable=False)
    counterparty_iban = Column(String, nullable=True)
    counterparty_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
