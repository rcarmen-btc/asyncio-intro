import asyncio
import os
import time
from turtle import down
import requests


def timer(func):
    def inner(num_of_file, url):
        t0 = time.time()    
        func(num_of_file, url) 
        print(time.time() - t0)
    return inner


def get_file(url):

    r = requests.get(url, allow_redirects=True)
    return r


def write_file(response):

    dir = 'imgs/'
    file_name = os.path.join(dir, response.url.split('/')[-1])
    try:
        os.mkdir(dir, )
    except:
        pass
    with open(file_name, 'wb') as file:
        file.write(response.content)


@timer
def download(num, url):
    for i in range(num):
        write_file(get_file(url))

def main():
    url = 'https://loremflickr.com/1080/1080/girl/all'
    download(10, url)


if __name__ == '__main__':
    main()
