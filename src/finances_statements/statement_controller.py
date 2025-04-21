from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from uuid import UUID
from finances_statements.models import Statements
from finances_statements.schemas import StatementCreate, StatementUpdate


async def get_statement(db: AsyncSession, statement_id: UUID):
    result = await db.execute(select(Statements).where(Statements.id == statement_id))
    return result.scalar_one_or_none()


async def get_statements(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Statements).offset(skip).limit(limit))
    return result.scalars().all()


async def create_statement(db: AsyncSession, statement: StatementCreate):
    db_statement = Statements(**statement.model_dump())
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
        .values(**statement.dict())
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    return await get_statement(db, statement_id)


async def delete_statement(db: AsyncSession, statement_id: UUID):
    stmt = delete(Statements).where(Statements.id == statement_id)
    await db.execute(stmt)
    await db.commit()
