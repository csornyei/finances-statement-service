from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from finances_statements.db import get_db
from finances_statements import statement_controller, schemas


router = APIRouter()


@router.post("/statements/", response_model=schemas.StatementOut)
async def create_statement(
    statement: schemas.StatementCreate, db: AsyncSession = Depends(get_db)
):
    return await statement_controller.create_statement(db, statement)


@router.get("/statements/", response_model=list[schemas.StatementOut])
async def read_statements(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await statement_controller.get_statements(db, skip=skip, limit=limit)


@router.get("/statements/{statement_id}", response_model=schemas.StatementOut)
async def read_statement(statement_id: UUID, db: AsyncSession = Depends(get_db)):
    db_statement = await statement_controller.get_statement(db, statement_id)
    if db_statement is None:
        raise HTTPException(status_code=404, detail="Statement not found")
    return db_statement


@router.put("/statements/{statement_id}", response_model=schemas.StatementOut)
async def update_statement(
    statement_id: UUID,
    statement: schemas.StatementUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_statement = await statement_controller.get_statement(db, statement_id)
    if db_statement is None:
        raise HTTPException(status_code=404, detail="Statement not found")
    return await statement_controller.update_statement(db, statement_id, statement)


@router.delete("/statements/{statement_id}")
async def delete_statement(statement_id: UUID, db: AsyncSession = Depends(get_db)):
    db_statement = await statement_controller.get_statement(db, statement_id)
    if db_statement is None:
        raise HTTPException(status_code=404, detail="Statement not found")
    await statement_controller.delete_statement(db, statement_id)
    return {"ok": True}
