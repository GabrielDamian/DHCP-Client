from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR
from Commons.computer import Computer


WIFI_IP = Computer.get_wifi_ip_address()

CLIENT_SOURCE_ADDRESS = (WIFI_IP, 68)
CLIENT_DESTINATION_ADDRESS = ('255.255.255.255', 67)

CLIENT_SOCKET = socket(AF_INET, SOCK_DGRAM)
CLIENT_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
CLIENT_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
CLIENT_SOCKET.bind(CLIENT_SOURCE_ADDRESS)

SUBNET_MASKS = [f'/{i}' for i in range(0, 33)]
