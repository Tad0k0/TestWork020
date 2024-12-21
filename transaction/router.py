from http.client import responses

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from transaction.schemas import CreateTransaction, CreateTransactionResponse, GetStatisticsResponse, Transaction
from transaction.worker import c_worker, create_transaction_task
from transaction.crud import delete_transactions, get_transaction_count, get_top3_transactions, get_average_transactionamount

from database.core import get_async_session
from common.logger import logger

router = APIRouter()

@router.post("/transactions", response_model=CreateTransactionResponse)
async def create_transaction(transaction: CreateTransaction) -> str:
    """Create transaction"""
    try:
        transaction_dict = transaction.model_dump()
        task = create_transaction_task.delay(transaction_dict)
    except Exception as exp:
        logger.error(
            f"Can not to create task. In duration creating error occured: {exp}"
        )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't to create a task",
        )
    response = CreateTransactionResponse(
        task_id=str(task.id), message="Transaction received"
    )
    return response


@router.post("/transactions", response_model=CreateTransactionResponse)
async def create_transaction(transaction: CreateTransaction) -> str:
    """Create transaction"""
    try:
        transaction_dict = transaction.model_dump()
        task = create_transaction_task.delay(transaction_dict)
    except Exception as exp:
        logger.error(
            f"Can not to create task. In duration creating error occured: {exp}"
        )
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't to create a task",
        )
    response = CreateTransactionResponse(
        task_id=str(task.id), message="Transaction received"
    )
    return response


@router.delete("/transactions", status_code=status.HTTP_200_OK)
async def delete_transaction(db: AsyncSession = Depends(get_async_session)) -> str:
    """Delete all transactions"""
    c_worker.control.purge()
    result = await delete_transactions(db)
    return "Success"

@router.get("/statistics", response_model=GetStatisticsResponse)
async def get_statistics(db: AsyncSession = Depends(get_async_session)) -> str:
    """Get statistics"""
    transaction_count = await get_transaction_count(db)
    average_transactionamount = await get_average_transactionamount(db)
    top3_transactions = await get_top3_transactions(db)
    response = GetStatisticsResponse(
        total_transactions=transaction_count,
        average_transaction_amount=average_transactionamount,
        top_transactions=[]
    )
    logger.debug(top3_transactions)
    for row in top3_transactions:
        response.top_transactions.append(Transaction(transaction_id=row[0].id, amount=row[0].amount))
    return response