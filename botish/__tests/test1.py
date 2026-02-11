import asyncio

from botish.tasks.tasks import check_periods


async def main():
    await check_periods(["BTCUSDT"])
    pass


asyncio.run(main())
