import asyncio

from botish.tasks.tasks import gather_open_interest


async def main():
    await gather_open_interest()
    pass


asyncio.run(main())
