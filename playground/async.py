import asyncio

my_task = asyncio.Event()

async def done():
    await asyncio.sleep(5)
    my_task.set()

async def main():
    await my_task.wait()
    print('hello')

asyncio.run(done())
print("Yay")
asyncio.run(main())

# finally:
    # loop.run_until_complete(loop.shutdown_asyncgens())
    # loop.close()

"""
import asyncio



my_task = asyncio.Event()

def done():
    my_task.set()



async def wait_until_done():
    await my_task.wait()  # await until event would be .set()
    print("Finally, the task is done")


async def main():
    loop.call_later(delay=5, callback=done)
    await wait_until_done()


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

"""