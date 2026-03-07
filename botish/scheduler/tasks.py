import asyncio
import logging
from collections import defaultdict
from pymongo import DESCENDING

from botish.bot.bot import send_s
from botish.bot.texts import PERIODS
from botish.db.mongo import get_db
from botish.finance.adapters.binance import BinanceAdapter
from botish.scheduler.calc import CalcOpenInterestResult, calc_open_interest
from botish.user import User

type SendData = dict[int, list[str]]

INDEX_EXPIRE_SECONDS = 86400 + 300


async def gather_open_interest() -> None:
    logging.info("Выполняется сборка данных...")

    binance = BinanceAdapter()

    binance_symbols = await binance.get_all_symbols()
    logging.info(f"- Загружено валют ({len(binance_symbols)})")

    binance_open_interests = await binance.get_open_interests(binance_symbols)
    logging.info("- Данные загружены")

    async with get_db() as db:
        await db.open_interest.create_index("symbol")
        await db.open_interest.create_index(
            [("dt", DESCENDING)], expireAfterSeconds=INDEX_EXPIRE_SECONDS
        )

        await db.exchanges.update_one(
            {"name": "binance"}, {"$set": {"symbols": binance_symbols}}, upsert=True
        )
        if binance_open_interests:
            await db.open_interest.insert_many(
                [o.model_dump() for o in binance_open_interests]
            )

    logging.info("- Данные записаны")

    await check_periods()


async def check_periods() -> None:
    logging.info("Выполняется проверка периодов...")

    send_data: SendData = defaultdict(list)

    async with get_db() as db:
        db_symbols = await db.exchanges.find_one({"name": "binance"})
        symbols = db_symbols["symbols"]

        for period_value in PERIODS.values():
            # TODO @me: переработать алгоритм с period_up_users/period_down_users
            # Пользователей может быть много и тогда они будут дублироваться
            period_up_users = await User.get_with_period("period_up", period_value)
            period_down_users = await User.get_with_period("period_down", period_value)

            if not period_up_users and not period_down_users:
                logging.info(f"- Пропуск периода [{period_value}]")
                continue

            logging.info(f"- Расчёт периода [{period_value}] ...")

            for symbol in symbols:
                result = await calc_open_interest(db, symbol, period_value)
                if not result:
                    continue

                for user_up in period_up_users:
                    if result.percent >= user_up.settings.open_interest.percent_up:
                        send_data[user_up.chat_id].append(
                            get_open_interest_period_up_message(user_up, symbol, result)
                        )

                for user_down in period_down_users:
                    if (
                        result.percent < 0
                        and abs(result.percent)
                        >= user_down.settings.open_interest.percent_down
                    ):
                        send_data[user_down.chat_id].append(
                            get_open_interest_period_down_message(
                                user_down, symbol, result
                            )
                        )

    if len(send_data):
        await broadcast_to_users(send_data)


def get_open_interest_period_up_message(
    user: User, symbol: str, result: CalcOpenInterestResult
) -> str:
    value = round(result.last_value / 1000000, 4)
    message = f"📈<b>{symbol}</b> +{abs(result.percent)}% <i>{value}млн$</i>"

    return message


def get_open_interest_period_down_message(
    user: User, symbol: str, result: CalcOpenInterestResult
) -> str:
    value = round(result.last_value / 1000000, 4)
    message = f"📉<b>{symbol}</b> -{abs(result.percent)}% <i>{value}млн$</i>"

    return message


async def broadcast_to_users(data: SendData) -> None:
    logging.info("Выполняется широковещательная рассылка сообщений...")
    for chat_id, messages in data.items():
        summarized_user_messages = summarize_user_message(messages)
        for m in summarized_user_messages:
            await send_s(chat_id, m)
            await asyncio.sleep(1)


def summarize_user_message(messages: list[str]) -> list[str]:
    summarized_messages: list[str] = []

    _message = ""
    for message in messages:
        if len(_message + f"\n{message}") > 4096:
            summarized_messages.append(_message)
            _message = ""
        else:
            _message += f"\n{message}"

    if _message:
        summarized_messages.append(_message)

    return summarized_messages


async def delete_old_open_interest() -> None:
    # TODO @me
    pass
