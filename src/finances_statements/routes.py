from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from finances_shared.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from finances_statements import schemas, statement_controller
from finances_statements.logger import logger

router = APIRouter()


@router.post("/statements/", response_model=schemas.StatementOut)
async def create_statement(
    statement: schemas.StatementCreate, db: AsyncSession = Depends(get_db)
):
    try:
        created_statement = await statement_controller.create_statement(db, statement)

        return created_statement

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating statement: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/statements/", response_model=list[schemas.StatementExtended])
async def list_statements(
    params: schemas.StatementFilters = Depends(), db: AsyncSession = Depends(get_db)
):
    return await statement_controller.get_statements(db, filters=params)


@router.get("/statements/{statement_id}", response_model=schemas.StatementExtended)
async def get_one_statement(statement_id: UUID, db: AsyncSession = Depends(get_db)):
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
