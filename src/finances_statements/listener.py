import asyncio
import json

import aio_pika
from finances_shared.db import get_db_session, init_db
from finances_shared.params import RabbitMQParams
from finances_shared.rabbitmq.listener import RabbitMQListener

from finances_statements import schemas, statement_controller
from finances_statements.logger import logger


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        payload = json.loads(message.body)

        try:
            statement = schemas.StatementCreate(**payload)
        except Exception as e:
            logger.error(f"Error parsing message: {e}")
            return

        async with get_db_session() as db:
            await statement_controller.create_statement(db, statement)
            logger.info(f"Statement created: {statement}")


async def main():
    init_db(logger)

    logger.info("Starting RabbitMQ listener...")

    params = RabbitMQParams.from_env(logger)

    listener = RabbitMQListener("statement")

    await listener.connect(params=params, logger=logger)

    await listener.listen(on_message, logger)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Stopping listener...")
    finally:
        loop.close()
