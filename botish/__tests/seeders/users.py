import asyncio
import random

from faker import Faker
from botish.user import User, UserSettings, OpenInterestSettings
from botish.bot.texts import PERIODS
from botish.db.mongo import db


fake = Faker("ru_RU")

COUNT = 5


async def main() -> None:
    users = []
    for i in range(0, COUNT):
        user = User(
            username=str(fake.simple_profile()["username"]),
            full_name=fake.name(),
            chat_id=random.randint(100000000, 900000000),
            settings=UserSettings(
                open_interest=OpenInterestSettings(
                    period_up=PERIODS[random.choice(list(PERIODS.keys()))],
                    period_down=PERIODS[random.choice(list(PERIODS.keys()))],
                    percent_up=random.randint(1, 100),
                    percent_down=random.randint(1, 100),
                )
            ),
        )
        users.append(user.model_dump())

    await db.users.insert_many(users)


asyncio.run(main())
