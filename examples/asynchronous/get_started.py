import asyncio
import logging
import time
import yaylib


async def main_serial():
    start_time = time.time()
    async with yaylib.AsyncClient(loglevel_stream=logging.DEBUG) as api:
        for i in range(10):
            await api.get_timeline(number=1)
    end_time = time.time()
    print(f"main_serial execution time: {end_time - start_time:.2f} seconds")


async def main_parallel():
    start_time = time.time()
    tasks = []
    async with yaylib.AsyncClient(loglevel_stream=logging.DEBUG) as api:
        for i in range(10):
            tasks.append(api.get_timeline(number=1))
        await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"main_parallel execution time: {end_time - start_time:.2f} seconds")


asyncio.run(main_serial())
asyncio.run(main_parallel())
