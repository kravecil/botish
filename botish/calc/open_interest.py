from dataclasses import dataclass
from datetime import timedelta

from botish.db.mongo import db


@dataclass
class CalcOpenInterestResult:
    last_value: float
    delta_value: float
    percent: float


async def calc_open_interest(
    symbol: str, period_value: int
) -> CalcOpenInterestResult | None:
    last_doc = await db.open_interest.find_one({"symbol": symbol}, sort=[("dt", -1)])

    if not last_doc:
        return None

    delta_dt = last_doc["dt"] - timedelta(minutes=period_value)
    delta_doc = await db.open_interest.find_one(
        {"symbol": symbol, "dt": {"$lt": delta_dt}}, sort=[("dt", -1)]
    )

    if not delta_doc:
        return None

    last_val = last_doc["value"]
    delta_val = delta_doc["value"]
    percent = round((last_val - delta_val) / delta_val * 100, 2)

    return CalcOpenInterestResult(
        last_value=last_val,
        delta_value=delta_val,
        percent=percent,
    )
