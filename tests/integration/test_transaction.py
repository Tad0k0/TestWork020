import pytest

from time import sleep
from common.logger import logger
from sqlalchemy import select

from transaction.models import Transactions

@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_create_transaction(client, get_async_session):
    """Create a transaction and check that it's in a db"""
    new_transaction = {
        "transaction_id": "123456",
        "user_id": "user_001",
        "amount": 100,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    logger.debug("Getting response from app")
    response = await client.post("/transactions", json=new_transaction)
    assert response.status_code == 200
    statement = select(Transactions.id).where(Transactions.id == new_transaction["transaction_id"])
    sleep(0.05) #For celery
    result = await get_async_session.execute(statement)
    transaction_id = result.fetchone()[0]
    logger.debug(f"Gets a transaction_id from db: {transaction_id}")
    assert transaction_id == new_transaction["transaction_id"]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_transaction"])
async def test_get_statistics(client, get_async_session):
    """Create a transaction and check that it's in a db"""
    transaction_2 = {
        "transaction_id": "123452",
        "user_id": "user_001",
        "amount": 200,
        "currency": "USD",
        "timestamp": "2024-12-12T12:01:00"
    }
    transaction_3 = {
        "transaction_id": "123453",
        "user_id": "user_001",
        "amount": 300,
        "currency": "USD",
        "timestamp": "2024-12-12T12:02:00",
    }
    transaction_4 = {
        "transaction_id": "123454",
        "user_id": "user_001",
        "amount": 400,
        "currency": "USD",
        "timestamp": "2024-12-12T12:03:00",
    }
    transactions=["123452", "123453", "123454"]
    logger.debug("Getting response from app")
    await client.post("/transactions", json=transaction_2)
    await client.post("/transactions", json=transaction_3)
    await client.post("/transactions", json=transaction_4)
    sleep(0.05)  # For celery
    response = await client.get("/statistics")
    assert response.status_code == 200
    assert response.json()["average_transaction_amount"] == 250.0
    assert response.json()["total_transactions"] == 4
    for transaction in response.json()["top_transactions"]:
        assert transaction["transaction_id"] in transactions

@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_get_statistics"])
async def test_delete_transactions(client):
    """Return a new registered user."""
    response = await client.delete("/transactions")
    logger.debug(response)
    assert response.status_code == 200
