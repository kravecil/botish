from dataclasses import dataclass
from datetime import datetime, timedelta

from botish.db.mongo import get_db


@dataclass
class CalcOpenInterestResult:
    last_value: float
    old_value: float
    percent: float

    last_dt: datetime
    old_dt: datetime


async def calc_open_interest(
    symbol: str, period_value: int
) -> CalcOpenInterestResult | None:
    async with get_db() as db:
        last_doc = await db.open_interest.find_one(
            {"symbol": symbol}, sort=[("dt", -1)]
        )

        if not last_doc:
            return None

        last_dt = last_doc["dt"]
        delta_dt = last_dt - timedelta(minutes=period_value)
        old_doc = await db.open_interest.find_one(
            {"symbol": symbol, "dt": {"$lt": delta_dt}}, sort=[("dt", -1)]
        )

        if not old_doc:
            return None

        last_val = last_doc["value"]
        old_val = old_doc["value"]
        percent = round((last_val - old_val) / old_val * 100, 2)

        old_dt = old_doc["dt"]

    return CalcOpenInterestResult(
        last_value=last_val,
        old_value=old_val,
        percent=percent,
        last_dt=last_dt,
        old_dt=old_dt,
    )
