from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Transactions
from transaction.schemas import CreateTransaction

from common.logger import logger

async def insert_transaction(session: AsyncSession, transaction: CreateTransaction):
    try:
        logger.debug(f"Session has type: {type(session)}")
        transaction_insert = Transactions(
            id=transaction["transaction_id"],
            user_id=transaction["user_id"],
            amount=transaction["amount"],
            currency=transaction["currency"],
            timestamp=transaction["timestamp"]
        )
        session.add(transaction_insert)
        await session.commit()
    except Exception as exp:
        await session.rollback()
        raise exp
    finally:
        await session.close()

async def delete_transactions(session: AsyncSession):
    try:
        statement = delete(Transactions)
        await session.execute(statement)
        await session.commit()
    except Exception as exp:
        await session.rollback()
        raise exp
    finally:
        await  session.close()
    return True

async def get_top3_transactions(session: AsyncSession):
    statement = select(Transactions).limit(3).order_by(Transactions.amount.desc())
    rows = await session.execute(statement)
    result = rows.fetchall()
    return result

async def get_transaction_count(session: AsyncSession):
    statement = select(func.count(Transactions.id))
    row = await session.execute(statement)
    result = row.fetchone()[0]
    return result

async def get_average_transactionamount(session: AsyncSession):
    statement = select(func.avg(Transactions.amount))
    row = await session.execute(statement)
    result = row.fetchone()[0]
    logger.debug(result)
    return result

