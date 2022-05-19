import socket
from urllib import response


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(('localhost', 8000))
sock.listen()


while True:
    
    print('Before accept')
    cli_sock, addr = sock.accept()
    print(f'Connection from {addr}')

    while True:
        print('Before recv')
        req = cli_sock.recv(4096)

        if not req:
            break
        else:
            print(req)
            response = 'Hello world\n'.encode()
            cli_sock.send(response)

    cli_sock.close()