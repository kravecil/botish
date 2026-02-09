import asyncio
import random

from faker import Faker
from botish.user import User
from botish.bot.texts import PERIODS
from botish.db import db

fake = Faker("ru_RU")

COUNT = 5


async def main() -> None:
    for i in range(0, COUNT):
        user_data = {
            "username": fake.simple_profile()["username"],
            "full_name": fake.name(),
            "chat_id": random.randint(100000000, 900000000),
            "settings": {
                "open_interest": {
                    "period_up": PERIODS[random.choice(PERIODS.keys())],
                }
            },
        }

        # TODO insert to db

        pass


asyncio.run(main())
