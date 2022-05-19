import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('localhost', 8000))
    sock.listen()
    
    selector.register(fileobj=sock, events=selectors.EVENT_READ, data=accept_connection)

def accept_connection(sock):

    cli_sock, addr = sock.accept()
    print(f'Connection from {addr}')

    selector.register(fileobj=cli_sock, events=selectors.EVENT_READ, data=send_message)


def send_message(cli_sock):

    req = cli_sock.recv(4096)

    if req:
        response = 'Hello world\n'.encode()
        cli_sock.send(response)
    else:
        selector.unregister(cli_sock)
        cli_sock.close()


def event_loop():

    while True:
        
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)
        

if __name__ == '__main__':
    server()
    event_loop()