import asyncio
import logging
import sys
import time

from botish.scheduler.tasks import gather_open_interest

TICK_TIME = 60  # seconds


async def main():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    while True:
        logging.info("Начинается обработка:")
        start_time = time.perf_counter()

        await gather_open_interest()

        exec_time = time.perf_counter() - start_time
        time_to_wait = max(0, TICK_TIME - exec_time)

        logging.info(
            f"Обработка завершена за {round(exec_time, 1)} сек! Пауза {round(time_to_wait, 1)} сек..."
        )
        await asyncio.sleep(time_to_wait)


asyncio.run(main())
