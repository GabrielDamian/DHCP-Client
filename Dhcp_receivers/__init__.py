from Dhcp.packet import Packet
from Dhcp.message_type import MessageType
from Dhcp.opcodes import Opcodes
import socket
from select import select
from typing import Optional


def offer_receiver(sock: socket.socket, timeout: int = 5) -> Optional[Packet]:
    while True:
        message_received, _, _ = select([sock], [], [], timeout)
        packet = Packet(sock.recv(1024)) if message_received else None
        if packet is None:
            return None
        if packet.opcode == Opcodes.REPLY and packet.dhcp_message_type == MessageType.OFFER:
            return packet
        packet = None


def ack_receiver(sock: socket.socket, timeout: int = 5) -> Optional[Packet]:
    while True:
        message_received, _, _ = select([sock], [], [], timeout)
        packet = Packet(sock.recv(1024)) if message_received else None
        if packet is None:
            return None
        if packet.opcode == Opcodes.REPLY and packet.dhcp_message_type == MessageType.ACK:
            return packet
        packet = None
