# from typing import Generator, Any
from contextlib import asynccontextmanager

from pymongo import AsyncMongoClient

from botish.settings import settings


class MongoDatabase:
    client: AsyncMongoClient

    def __init__(self) -> None:
        usr = settings.db_username
        pwd = settings.db_password
        host = settings.db_host
        port = settings.db_port
        name = settings.db_name

        db_dsn = f"mongodb://{usr}:{pwd}@{host}:{port}/{name}?authSource=admin"
        self.client = AsyncMongoClient(db_dsn)

    async def close(self) -> None:
        await self.client.close()

    @property
    def db(self):
        return self.client[settings.db_name]

    @property
    def open_interest(self):
        return self.db["open_interest"]

    @property
    def users(self):
        return self.db["users"]

    @property
    def exchanges(self):
        return self.db["exchanges"]


@asynccontextmanager
async def get_db():
    db = MongoDatabase()
    try:
        yield db
    finally:
        await db.close()
