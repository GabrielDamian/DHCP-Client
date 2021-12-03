import socket
import threading
import time
from DHCP_Packet import *
SOURCE_PORT = 68
DESTINATION_PORT = 67
SOURCE_ADDR = ("", SOURCE_PORT)
DESTINATIN_ADDR = ('<broadcast>', DESTINATION_PORT)


def init_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SOURCE_ADDR)
    return sock


if __name__ == "__main__":

    sock = init_socket()

    #construire packet DHCP Discover
    packet = Packet(requested_options=[Optiuni_request.SUBNET_MASK, Optiuni_request.DOMAIN_SERVER])
    packet.opcode = Opcodes.REQUEST
    packet.host_name = "salut"
    packet.dhcp_message_type = Tip_Mesaj.DISCOVER
    packet.boot_flags = 1
    print(packet)

    packet_bytes = packet.pregateste_packetul()

    sock.sendto(packet_bytes, DESTINATIN_ADDR)    #trimitere DISCOVER

    # #*logica de asteptare*
    # mesaj_server = sock.recv(1024)
    # packet_2 = Packet(mesaj_server)
    #
    # if packet_2.dhcp_message_type == Tip_Mesaj.OFFER:
    #     packet_2.opcode = Opcodes.REQUEST
    #     packet_2.dhcp_message_type = Tip_Mesaj.REQUEST
    #     sock.sendto(packet_2.pregateste_packetul(), DESTINATIN_ADDR)
    #
    #     # *logica de asteptare*
    #     mesaj_ack = sock.recv(1024)
    #     packet_ack = Packet(mesaj_ack)
    #     if packet_ack.dhcp_message_type == Tip_Mesaj.ACK:
    #         print(packet_ack)


 