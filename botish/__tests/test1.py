import asyncio

from botish.tasks.tasks import check_periods

COUNT=1

async def main():
    await check_periods()
    pass


asyncio.run(main())
