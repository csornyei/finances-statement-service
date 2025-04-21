import os

from finances_statements.logger import logger


def get_database_connection() -> str:
    """
    Get the file handler type from environment variables.
    - POSTGRES_HOST=postgres
    - POSTGRES_PORT=5432
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres

    """
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    if not db_host or not db_port or not db_user or not db_password or not db_name:
        logger.error(
            "Database connection parameters are not set in environment variables."
        )
        raise ValueError(
            "Database connection parameters are not set in environment variables."
        )

    return f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_rabbitmq_connection() -> str:
    """
    Get the RabbitMQ connection string from environment variables.
    - RABBITMQ_HOST=rabbitmq
    - RABBITMQ_PORT=5672
    - RABBITMQ_USER=guest
    - RABBITMQ_PASSWORD=guest
    """
    rabbitmq_host = os.getenv("RABBITMQ_HOST")
    rabbitmq_port = os.getenv("RABBITMQ_PORT")
    rabbitmq_user = os.getenv("RABBITMQ_USER")
    rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")

    if (
        not rabbitmq_host
        or not rabbitmq_port
        or not rabbitmq_user
        or not rabbitmq_password
    ):
        logger.error(
            "RabbitMQ connection parameters are not set in environment variables."
        )
        raise ValueError(
            "RabbitMQ connection parameters are not set in environment variables."
        )

    return (
        f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"
    )
