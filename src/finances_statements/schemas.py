from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class StatementBase(BaseModel):
    date: datetime
    interest_date: datetime
    amount: int
    counterparty_iban: Optional[str] = None
    counterparty_name: Optional[str] = None
    description: Optional[str] = None


class StatementCreate(StatementBase):
    account: str


class StatementUpdate(StatementBase):
    pass


class StatementOut(StatementBase):
    id: UUID
    account_iban: str
    account_name: str

    class Config:
        from_attributes = True


class StatementAccount(BaseModel):
    iban: str
    name: str
    nickname: str

    class Config:
        from_attributes = True


class StatementTag(BaseModel):
    id: UUID
    name: str
    color: str

    class Config:
        from_attributes = True


class StatementExtended(StatementOut):
    source_account: Optional[StatementAccount] = None
    destination_account: Optional[StatementAccount] = None
    tags: Optional[list[StatementTag]] = None

    class Config:
        from_attributes = True


class StatementFilters(BaseModel):
    before_date: Optional[datetime] = None
    after_date: Optional[datetime] = None
    account_iban: Optional[str] = None
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None
    limit: int = 100
    skip: int = 0
