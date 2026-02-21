import asyncio

from botish.bot.bot import send_s
from botish.bot.texts import PERIODS
from botish.calc.open_interest import calc_open_interest, CalcOpenInterestResult
from botish.db.mongo import get_db
from botish.finance.adapters.binance import BinanceAdapter
from botish.tasks.broker import broker
from botish.user import User


@broker.task(schedule=[{"interval": 60}])
async def gather_open_interest() -> None:
    binance = BinanceAdapter()

    binance_symbols = await binance.get_all_symbols()
    binance_open_interests = await binance.get_open_interests(binance_symbols)

    async with get_db() as db:
        await db.exchanges.update_one(
            {"name": "binance"}, {"$set": {"symbols": binance_symbols}}
        )
        await db.open_interest.insert_many(
            [o.model_dump() for o in binance_open_interests]
        )

    await check_periods.kiq(binance_symbols)


@broker.task
async def check_periods(symbols: list[str]) -> None:
    tasks_to_send = []

    sem = asyncio.Semaphore(20)

    for period_value in PERIODS.values():
        # TODO @me: переработать алгоритм с period_up_users/period_down_users
        # Пользователей может быть много и тогда они будут дублироваться
        period_up_users = await User.get_with_period("period_up", period_value)
        period_down_users = await User.get_with_period("period_down", period_value)

        for symbol in symbols:
            result = await calc_open_interest(symbol, period_value)
            if not result:
                continue

            for user_up in period_up_users:
                if result.percent >= user_up.settings.open_interest.percent_up:
                    tasks_to_send.append(
                        send_open_interest_period_up(sem, user_up, symbol, result)
                    )

            for user_down in period_down_users:
                pass
                if (
                    result.percent < 0
                    and abs(result.percent)
                    >= user_down.settings.open_interest.percent_down
                ):
                    tasks_to_send.append(
                        send_open_interest_period_down(sem, user_down, symbol, result)
                    )

    await asyncio.gather(*tasks_to_send)


async def send_open_interest_period_up(
    sem: asyncio.Semaphore, user: User, symbol: str, result: CalcOpenInterestResult
) -> None:
    message = (
        f"📈Binance <b>{symbol}</b> (период: {user.settings.open_interest.period_up_h}\n"
        "-----------------------\n"
        f"<b>Рост:</b> +{abs(result.percent)}% ({round(result.last_value / 1000000, 4)}млн $)\n"
        f"Дата: {result.last_dt:%d.%m.%Y %H:%M:%S}\n"
        f"<i>Прежнее значение: {round(result.old_value / 1000000, 4)}млн $ от {result.old_dt:%d.%m.%Y %H:%M:%S}</i>"
    )

    await send_s(sem, user.chat_id, message)
    # print(message)

    await asyncio.sleep(0.3)


async def send_open_interest_period_down(
    sem: asyncio.Semaphore, user: User, symbol: str, result: CalcOpenInterestResult
) -> None:
    message = (
        f"📈Binance <b>{symbol}</b> (период: {user.settings.open_interest.period_down_h}\n"
        "-----------------------\n"
        f"<b>Просадка:</b> +{abs(result.percent)}% ({round(result.last_value / 1000000, 4)}млн $)\n"
        f"Дата: {result.last_dt:%d.%m.%Y %H:%M:%S}\n"
        f"<i>Прежнее значение: {round(result.old_value / 1000000, 4)}млн $ от {result.old_dt:%d.%m.%Y %H:%M:%S}</i>"
    )

    await send_s(sem, user.chat_id, message)
    # print(message)

    await asyncio.sleep(0.3)
