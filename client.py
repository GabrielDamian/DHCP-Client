import socket
import threading
import time

PORT = 8080
ADRESS = ""
ADDR = (ADRESS,PORT)
FORMAT = "utf-8"

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ADRESS, PORT))

    while True:
        sock.sendto(b"Hello",('<broadcast>',PORT))
        print("Trimis Hello")
        time.sleep(5)