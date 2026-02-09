import asyncio

from botish.tasks.tasks import check_periods


async def main():
    await check_periods()
    pass


asyncio.run(main())
