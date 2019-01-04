import asyncio
from aliu.debug.placeholder import Placeholder, add_placeholder, originof

def run_tasks(*tasks):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

async def generator( n = 100 ):
    for data in range(n):
        await asyncio.sleep(.001)
        yield data

async def do_something():
    async for i in generator():
        print(i)

def test_async():
    coroutine_func = Placeholder(do_something)
    coroutine = Placeholder(do_something())
    run_tasks(coroutine_func(), coroutine)
