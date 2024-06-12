import time
import asyncio
import aiohttp
from collections.abc import Coroutine, Iterable

SOURCE = "http://127.0.0.1:5000/"


async def gather_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(SOURCE) as response:
            result = await response.json()
            return result["value"]


async def gather_data_and_add_param(*args) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(SOURCE) as response:
            result = await response.json()
            return f"{result['value']}+{args}"
    

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


async def do_async_tasks(function: Coroutine, parameters: Iterable) -> list:
    param_and_task_pairs = [(param, asyncio.create_task(function(*param))) for param in parameters]
    return [(param, await task) for (param, task) in param_and_task_pairs]


async def run_commands(commands: list) -> list:
    command_result_list = []
    processes = []
    for cmd_and_args in commands:
        cmd = cmd_and_args[0]
        args = cmd_and_args[1]
        proc = await asyncio.create_subprocess_exec(
            cmd,
            args,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        processes.append((cmd, proc))

    for (cmd, proc) in processes:
        stdout, stderr = await proc.communicate()
        print(f"{cmd}: {stdout.decode()}")
        command_result_list.append((cmd, stdout.decode()))
    
    return command_result_list


def main():
    start = time.perf_counter()
    asyncio.run(process_projects(10))
    
    params = [[1, 2], [3, 4], [5, 6], [7, 8, 9]]
    result = asyncio.run(do_async_tasks(gather_data_and_add_param, params))
    print(result)
    
    command_result_list = asyncio.run(run_commands(
        [['ls', '-la'], ['ls', '-latr'], ['sleep', '3'], ['sleep', '6']]
    ))
    
    run_length = time.perf_counter() - start
    print(f"Execution took {run_length} seconds")


if __name__ == "__main__":
    main()
    