import os
from socket import socket
from time import time
import aiohttp
import asyncio


def write_image(data):
    dir = 'imgs/'
    try:
        os.mkdir(dir, )
    except:
        pass
    file_name = f'{dir}file-{int(time() * 1000)}.jpg'
    with open(file_name, 'wb') as file:
        file.write(data)

async def fetch_content(url, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as resp:
        data = await resp.read()
        write_image(data)


async def main():
    url = 'https://loremflickr.com/1080/1080/girl/all'
    tasks = []    

    async with aiohttp.ClientSession() as sess:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, sess))    
            tasks.append(task)
    
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time() - t0)