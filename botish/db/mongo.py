# from typing import Generator, Any
from contextlib import asynccontextmanager

from pymongo import AsyncMongoClient

from botish.settings import settings


class MongoDatabase:
    client: AsyncMongoClient

    def __init__(self, db_dsn: str) -> None:
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
    db = MongoDatabase(settings.db_dsn.encoded_string())
    try:
        yield db
    finally:
        await db.close()
