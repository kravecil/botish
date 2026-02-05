from pydantic import BaseModel

from botish.db.mongo import db


class OpenInterestSettings(BaseModel):
    period_up: int | None = None
    percent_up: float | None = None

    period_down: int | None = None
    percent_down: float | None = None


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

    @staticmethod
    async def get(chat_id: int) -> "User":
        user_db = await db.users.find_one({"chat_id": chat_id})

        return User(**user_db)

    async def update_period_up(self, value: int) -> None:
        await db.users.update_one(
            filter={"chat_id": self.chat_id},
            update={"$set": {"settings.open_interest.period_up": value}},
        )
