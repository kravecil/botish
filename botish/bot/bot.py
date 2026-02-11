import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ChatIdUnion

from botish.settings import settings

bot = Bot(
    token=settings.telegram_bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def send(chat_id: ChatIdUnion, message: str) -> None:
    await bot.send_message(chat_id, message)


async def send_s(
    semaphore: asyncio.Semaphore, chat_id: ChatIdUnion, message: str
) -> None:
    async with semaphore:
        await send(chat_id, message)
