from pydantic import BaseModel

from botish.db.mongo import db
from botish.bot.texts import PERIODS


class OpenInterestSettings(BaseModel):
    period_up: int = 1
    percent_up: int = 5

    period_down: int = 1
    percent_down: int = 5

    @property
    def period_up_h(self) -> str:
        return next(iter(k for k, v in PERIODS.items() if v == self.period_up), "")

    @property
    def period_down_h(self) -> str:
        return next(iter(k for k, v in PERIODS.items() if v == self.period_down), "")


class UserSettings(BaseModel):
    open_interest: OpenInterestSettings


class User(BaseModel):
    chat_id: int

    username: str | None
    full_name: str | None

    settings: UserSettings

    @staticmethod
    async def register(
        chat_id: int,
        username: str | None,
        full_name: str | None,
    ) -> "User":
        user = User(
            chat_id=chat_id,
            username=username,
            full_name=full_name,
            settings=UserSettings(open_interest=OpenInterestSettings()),
        )
        filter = {"chat_id": chat_id}
        update = {"$set": {**user.model_dump()}}

        await db.users.update_one(filter=filter, update=update, upsert=True)

        return user

    # async def save(self) -> None:
    #     await db.users.update_one(
    #         {"chat_id": self.chat_id}, {"$set": {**self.model_dump()}}, upsert=True
    # )

    @staticmethod
    async def all() -> list[User]:
        db_users = db.users.find()

        return [User(**user) async for user in db_users]

    @staticmethod
    async def get(chat_id: int) -> "User":
        user_db = await db.users.find_one({"chat_id": chat_id})

        return User(**user_db)

    async def update_settings(self, name: str, value: int | float) -> None:
        await db.users.update_one(
            filter={"chat_id": self.chat_id},
            update={"$set": {name: value}},
        )

    async def update_period_up(self, value: int) -> None:
        await self.update_settings("settings.open_interest.period_up", value)

    async def update_period_down(self, value: int) -> None:
        await self.update_settings("settings.open_interest.period_down", value)

    async def update_percent_up(self, value: float) -> None:
        await self.update_settings("settings.open_interest.percent_up", value)

    async def update_percent_down(self, value: float) -> None:
        await self.update_settings("settings.open_interest.percent_down", value)

    @staticmethod
    async def get_with_period(key: str, value: int) -> list[User]:
        db_users = db.users.find({f"settings.open_interest.{key}": value})

        return [User(**u) async for u in db_users]
