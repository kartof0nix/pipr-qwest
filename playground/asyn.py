import asyncio

async def route():
    print('oh')
    await asyncio.sleep(5)
    print('hello')


async def main():
    t1 = asyncio.create_task(route())
    await asyncio.sleep(1)
    print("Hiii")
    await t1
    
asyncio.run(main())