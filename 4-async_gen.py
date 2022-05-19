from asyncio import tasks
from os import read
from pydoc import cli
import socket
from select import select


tasks = []

to_read = {}
to_write = {}


def accept_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('localhost', 8000))
    sock.listen()

    while True:
        
        yield ('read', sock)     
        cli_sock, addr = sock.accept()

        print(f'Connection from {addr}')

        tasks.append(send_message(cli_sock))


def send_message(cli_sock):

    while True:

        yield ('read', cli_sock)
        req = cli_sock.recv(4096)

        if not req:
            break
        else:
            response = 'Hello world\n'.encode()
            yield ('write', cli_sock)
            cli_sock.send(response)

    cli_sock.close()


def event_loop():
    
    while any([tasks, to_read, to_write]):
        print('======= 3. We have any of tasks, to_read or to_write ')
        while not tasks:
            
            print('<<<<<>>>>>> No tasks, waiting request from client... <<<<<>>>>>>')
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for s in ready_to_read:
                print('=======   {-} Pop from to_read ')
                print('=======   [+] Adding to_read tasks ')
                tasks.append(to_read.pop(s))

            for s in ready_to_write:
                print('=======    {-} Pop from to_write ')
                print('=======    [+] Adding to_write tasks ')
                tasks.append(to_write.pop(s))
        
        try:
            task = tasks.pop(0)
            print('=======    [-] Pop task ')
            reason, s = next(task)
            print(f'----------Go to next yield {reason}------------')
            if reason == 'read':
                print('=======    {+} Adding to to_read ')
                to_read[s] = task
            if reason == 'write':
                print('=======    {+} Adding to to_write ')
                to_write[s] = task

        except StopIteration:
            print('Done!')
            

print('======= 1. [+] Add accept_connection task to tasks ')
tasks.append(accept_connection())
print('======= 2. Go into event loop ')
event_loop()