import asyncio

from botish.tasks.tasks import check_periods, gather_open_interest


async def main():
    # await gather_open_interest()
    await check_periods()
    pass


asyncio.run(main())
