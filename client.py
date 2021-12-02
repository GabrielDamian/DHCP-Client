import socket
import threading
import time
from DHCP_Packet import *
PORT = 8080
ADRESS = ""
ADDR = ('<broadcast>', PORT)
FORMAT = "utf-8"


def init_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ADRESS, PORT))
    return sock


if __name__ == "__main__":

    sock = init_socket()


    #construire packet DHCP Discover
    packet = Packet(requested_options=[Optiuni_request.SUBNET_MASK, Optiuni_request.DOMAIN_SERVER])
    packet.opcode = Opcodes.REQUEST
    packet.host_name = "salut"
    packet.dhcp_message_type = Tip_Mesaj.DISCOVER

    packet_bytes = packet.pregateste_packetul()

    #trimitere DISCOVER
    sock.sendto(packet_bytes, ADDR)

    mesaj_server = sock.recv(1000)
    packet_2 = Packet(mesaj_server)

    if packet_2.dhcp_message_type == Tip_Mesaj.OFFER:
        packet_2.opcode = Opcodes.REQUEST
        packet_2.dhcp_message_type = Tip_Mesaj.REQUEST
        sock.sendto(packet_2.pregateste_packetul(), ADDR)

    mesaj_ack = sock.recv(1000)
    packet_ack = Packet(mesaj_ack)
    if packet_ack.dhcp_message_type == Tip_Mesaj.ACK:
        print(packet_ack)


 