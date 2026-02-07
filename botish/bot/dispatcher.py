from aiogram import Dispatcher

from botish.bot.handlers import router as handlers_router
from botish.bot.states import router as states_router

dp = Dispatcher()


dp.include_router(handlers_router)
dp.include_router(states_router)
