import asyncio
import logging
from enum import StrEnum
from typing import Any

from pydantic import HttpUrl

from botish.finance.adapters.interface import IAdapter
from botish.finance.models.open_interest import OpenInterest
from botish.settings import settings
from botish.utils.dt import from_timestamp_ms
from botish.utils.http import fetch

FAPI_URL = "https://fapi.binance.com"


class SymbolStatus(StrEnum):
    trading = "TRADING"


class BinanceAdapter(IAdapter):
    token: str

    def __init__(self) -> None:
        self.token = settings.binance_api_token.get_secret_value()

    async def get_all_symbols(self) -> list[str]:
        symbols: list[str] = []

        try:
            url = HttpUrl(f"{FAPI_URL}/fapi/v1/exchangeInfo")
            data = await fetch(url)

            _symbols: list[dict[str, Any]] = data["symbols"]

            symbols = [
                s["symbol"] for s in _symbols if s["status"] == SymbolStatus.trading
            ]
        except Exception as e:
            logging.error(f"Не удалось загрузить монеты Binance. Ошибка: {e!s}")

        return symbols

    async def get_open_interests(self, symbols: list[str]) -> list[OpenInterest]:
        url = HttpUrl(f"{FAPI_URL}/fapi/v1/openInterest")

        tasks = []

        for symbol in symbols:
            params = {
                "symbol": symbol,
            }

            tasks.append(fetch(url, params))

        task_results = await asyncio.gather(*tasks, return_exceptions=True)

        return [
            self._process_result_open_interest(r)
            for r in task_results
            if not isinstance(r, Exception)
        ]

    @staticmethod
    def _process_result_open_interest(result) -> OpenInterest:
        return OpenInterest(
            symbol=result["symbol"],
            value=float(result["openInterest"]),
            dt=from_timestamp_ms(result["time"]),
        )
