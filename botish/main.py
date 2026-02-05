import asyncio
import logging
import sys

from botish.bot.bot import bot
from botish.bot.dispatcher import dp


async def main():
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

asyncio.run(main())
