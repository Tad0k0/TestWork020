from celery import Celery

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from transaction.crud import insert_transaction
from transaction.schemas import CreateTransaction

from config import settings
from common.logger import logger

loop = asyncio.get_event_loop()

c_worker = Celery(__name__)
c_worker.conf.broker_url = settings.redis_url

c_worker.log.setup_handlers(logger,
                        logfile="celery.log",
                        format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
                        colorize=False)
c_worker.log.redirect_stdouts_to_logger(logger)
c_worker.conf.update(worker_hijack_root_logger=False)


engine = create_async_engine(settings.db_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def async_session_inject(async_crud, *arg):
    async with async_session_maker() as session:
        logger.debug(type(session))
        return await async_crud(session, *arg)




@c_worker.task(name="create_task")
def create_transaction_task(transaction: CreateTransaction):
    loop.run_until_complete(async_session_inject(insert_transaction, transaction))
    return True