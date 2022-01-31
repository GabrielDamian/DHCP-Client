from socket import socket
from typing import Optional
from select import select
from Dhcp.packet import Packet
from Dhcp.opcodes import Opcodes
from Dhcp.message_type import MessageType


class Receivers:

    @staticmethod
    def discover_receiver(sock: socket, timeout: int = 5) -> Optional[Packet]:
        """
        Waits for an DHCP discover packet, captures it and returns it
        :param sock: socket from which to listen
        :param timeout: amount of time to listen until gives up
        :return: DHCP discover packet received or None if times out
        """
        while True:
            message_received, _, _ = select([sock], [], [], timeout)
            packet = Packet(sock.recv(1024)) if message_received else None
            if packet is None:
                return None
            if packet.opcode == Opcodes.REQUEST and packet.dhcp_message_type == MessageType.DISCOVER:
                return packet
            packet = None

    @staticmethod
    def offer_receiver(sock: socket, timeout: int = 5) -> Optional[Packet]:
        """
        Waits for an DHCP offer packet, captures it and returns it
        :param sock: socket from which to listen
        :param timeout: amount of time to listen until gives up
        :return: DHCP offer packet received or None if times out
        """
        while True:
            message_received, _, _ = select([sock], [], [], timeout)
            packet = Packet(sock.recv(1024)) if message_received else None
            if packet is None:
                return None
            if packet.opcode == Opcodes.REPLY and packet.dhcp_message_type == MessageType.OFFER:
                return packet
            packet = None

    @staticmethod
    def request_receiver(sock: socket, timeout: int = 5) -> Optional[Packet]:
        """
        Waits for an DHCP request packet, captures it and returns it
        :param sock: socket from which to listen
        :param timeout: amount of time to listen until gives up
        :return: DHCP request packet received or None if times out
        """
        while True:
            message_received, _, _ = select([sock], [], [], timeout)
            packet = Packet(sock.recv(1024)) if message_received else None
            if packet is None:
                return None
            if packet.opcode == Opcodes.REQUEST and packet.dhcp_message_type == MessageType.REQUEST:
                return packet
            packet = None

    @staticmethod
    def ack_receiver(sock: socket, timeout: int = 5) -> Optional[Packet]:
        """
        Waits for an DHCP ack packet, captures it and returns it
        :param sock: socket from which to listen
        :param timeout: amount of time to listen until gives up
        :return: DHCP ack packet received or None if times out
        """
        while True:
            message_received, _, _ = select([sock], [], [], timeout)
            packet = Packet(sock.recv(1024)) if message_received else None
            if packet is None:
                return None
            if packet.opcode == Opcodes.REPLY and packet.dhcp_message_type == MessageType.ACK:
                return packet
            packet = None
