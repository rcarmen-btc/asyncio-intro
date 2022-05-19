from time import time


def gen(s):
    for i in s:
        yield i
        


def gen_file_name():
    while True:
        yield f'file-{int(time() * 1000)}.jpeg'

        
print(gen('Hello'))