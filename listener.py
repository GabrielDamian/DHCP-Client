import socket
import select
import threading
from sys import getsizeof

server = ''
port = 8080
addr = (server, port)

if __name__ == "__main__":
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(addr)

    while True:
        data = listener.recv(100)
        print(data)