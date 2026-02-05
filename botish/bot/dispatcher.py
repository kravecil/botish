from aiogram import Dispatcher

from botish.bot.handlers import router

dp = Dispatcher()


dp.include_router(router)
