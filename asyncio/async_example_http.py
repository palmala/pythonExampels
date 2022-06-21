import time
import asyncio
import aiohttp

SOURCE = "http://127.0.0.1:5000/"


async def gather_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(SOURCE) as response:
            result = await response.json()
            return result["value"]


async def generate_data(p):
    task1 = asyncio.create_task(gather_data())
    task2 = asyncio.create_task(gather_data())
    first_data = await task1
    second_data = await task2
    return [p, first_data, f"{p}{first_data}{second_data}"]


async def process_projects(number):
    projects = [f"project{i}" for i in range(number)]
    tasks = []
    for project in projects:
        tasks.append(asyncio.create_task(generate_data(project)))

    for task in tasks:
        print(await task)


def main():
    start = time.perf_counter()
    asyncio.run(process_projects(10))
    run_length = time.perf_counter() - start
    print(f"Execution took {run_length} seconds")


if __name__ == "__main__":
    main()
