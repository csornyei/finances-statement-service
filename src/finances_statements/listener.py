import asyncio
import json

import aio_pika

from finances_statements.logger import logger
from finances_statements.db import get_db
from finances_statements import statement_controller, schemas
from finances_statements.params import get_rabbitmq_connection


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body}")
        payload = json.loads(json.loads(message.body))

        print({"data": payload})

        try:
            statement = schemas.StatementCreate(**payload)
        except Exception as e:
            logger.error(f"Error parsing message: {e}")
            return

        db_generator = get_db()
        db = await anext(db_generator)
        try:
            await statement_controller.create_statement(db, statement)
            logger.info(f"Statement created: {statement}")
        finally:
            await db_generator.aclose()


async def main():
    conn_string = get_rabbitmq_connection()
    connection = await aio_pika.connect_robust(conn_string)
    channel = await connection.channel()
    queue = await channel.declare_queue("statement", durable=True)

    logger.info("Connected to RabbitMQ and declared queue")
    logger.info("Waiting for messages...")
    await queue.consume(on_message)

    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Stopping listener...")
    finally:
        loop.close()
