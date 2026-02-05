from botish.db.mongo import db
from botish.finance.adapters.binance import BinanceAdapter
from botish.tasks.broker import broker


@broker.task(schedule=[{"interval": 60}])
async def gather_open_interest() -> None:
    binance = BinanceAdapter()

    binance_open_interests = await binance.get_open_interests()

    await db.open_interest.insert_many([o.model_dump() for o in binance_open_interests])
