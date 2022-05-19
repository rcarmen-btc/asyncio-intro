import socket
from select import select


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(('localhost', 8000))
sock.listen()
to_monitor = []

def accept_connection(sock):

    cli_sock, addr = sock.accept()
    print(f'Connection from {addr}')

    to_monitor.append(cli_sock)
    

def send_message(cli_sock):

    req = cli_sock.recv(4096)

    if req:
        response = 'Hello world\n'.encode()
        cli_sock.send(response)
    else:
        cli_sock.close()


def event_loop():
    while True:
        
        ready_to_read, _, _ = select(to_monitor, [], [])
        for s in ready_to_read:
            print(s)
            if s is sock:
                accept_connection(s)
            else:
                send_message(s)


if __name__ == '__main__':
    to_monitor.append(sock)
    event_loop()
    # accept_connection(sock)