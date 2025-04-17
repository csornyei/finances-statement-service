from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class StatementBase(BaseModel):
    date: datetime
    interest_date: datetime
    amount: int
    account: str
    counterparty_iban: Optional[str] = None
    counterparty_name: Optional[str] = None
    description: Optional[str] = None


class StatementCreate(StatementBase):
    pass


class StatementUpdate(StatementBase):
    pass


class StatementOut(StatementBase):
    id: UUID

    class Config:
        orm_mode = True
