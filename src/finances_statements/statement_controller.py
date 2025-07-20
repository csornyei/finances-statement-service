from typing import Optional
from uuid import UUID

from finances_shared.models import Statements
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

import finances_statements.services.accounts as accounts_service
from finances_statements.logger import logger
from finances_statements.schemas import (
    StatementCreate,
    StatementExtended,
    StatementFilters,
    StatementUpdate,
)


async def get_statement(
    db: AsyncSession, statement_id: UUID
) -> Optional[StatementExtended]:
    result = await db.execute(
        select(Statements)
        .where(Statements.id == statement_id)
        .options(
            joinedload(Statements.source_account),
            joinedload(Statements.destination_account),
            selectinload(Statements.tags),
        )
    )

    statement = result.scalar_one_or_none()

    if not statement:
        return None

    statement = StatementExtended.model_validate(statement)
    return statement


async def get_statements(
    db: AsyncSession, filters: StatementFilters = StatementFilters()
):
    query = select(Statements)
    if filters.before_date:
        query = query.where(Statements.interest_date < filters.before_date)

    if filters.after_date:
        query = query.where(Statements.interest_date > filters.after_date)

    if filters.account_iban:
        query = query.where(Statements.account_iban == filters.account_iban)

    if filters.min_amount is not None:
        query = query.where(Statements.amount >= filters.min_amount)

    if filters.max_amount is not None:
        query = query.where(Statements.amount <= filters.max_amount)

    query = query.options(
        selectinload(Statements.source_account),
        selectinload(Statements.destination_account),
        selectinload(Statements.tags),
    )

    query = query.offset(filters.skip).limit(filters.limit)

    result = await db.execute(query)

    return result.scalars().all()


async def create_statement(db: AsyncSession, statement: StatementCreate):
    statement_dict = statement.model_dump()

    try:
        account_iban = statement_dict.pop("account")
        source_account = accounts_service.get_account_by_iban(account_iban)

        if not source_account:
            raise ValueError(f"Source account with IBAN {account_iban} not found.")

    # TODO: create better errors for this
    except ValueError as e:
        raise ValueError(f"Error fetching source account: {str(e)}")
    except Exception as e:
        raise ValueError(f"An error occurred while fetching source account: {str(e)}")

    source_account = source_account[0]

    statement_dict["account_iban"] = source_account["iban"]
    statement_dict["account_name"] = source_account["name"]

    try:
        destination_account = accounts_service.get_account_by_name_and_iban(
            statement.counterparty_name, statement.counterparty_iban
        )

        if not destination_account:
            accounts_service.create_account(
                {
                    "name": statement.counterparty_name,
                    "iban": statement.counterparty_iban,
                    "nickname": f"{statement.counterparty_name} ({statement.counterparty_iban})",
                }
            )
    except ValueError as e:
        logger.error(f"Error fetching destination account: {str(e)}")
        raise ValueError(f"Error fetching destination account: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred while fetching destination account: {str(e)}")
        raise ValueError(
            f"An error occurred while fetching destination account: {str(e)}"
        )

    db_statement = Statements(**statement_dict)
    db.add(db_statement)
    await db.commit()
    await db.refresh(db_statement)
    return db_statement


async def update_statement(
    db: AsyncSession, statement_id: UUID, statement: StatementUpdate
):
    stmt = (
        update(Statements)
        .where(Statements.id == statement_id)
        .values(**statement.model_dump())
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    return await get_statement(db, statement_id)


async def delete_statement(db: AsyncSession, statement_id: UUID):
    stmt = delete(Statements).where(Statements.id == statement_id)
    await db.execute(stmt)
    await db.commit()
