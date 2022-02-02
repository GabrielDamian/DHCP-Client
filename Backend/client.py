from Dhcp.packet import Packet
from Commons.computer import Computer
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR


class Client:
    def __init__(self):
        self._source_address = (Computer.get_wifi_ip_address(), 68)
        self._broadcast_address = ('255.255.255.255', 67)
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind(self._source_address)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def _send_message(self, message: Packet):
        """
        Broadcast a dhcp packet
        :param message: Packet that will be sent
        """
        self._socket.sendto(message.encode(), self._broadcast_address)
