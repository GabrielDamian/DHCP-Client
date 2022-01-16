from random import randint, choice
from DHCP_Client.dhcp_packet import Packet
from DHCP_Client.message_type import MessageType
from DHCP_Client.opcodes import Opcodes
from DHCP_Client import SERVER_SOCKET, SERVER_BROADCAST_ADDR
from typing import Optional


def random_ip() -> str:
    return f"{randint(60, 167)}.{randint(60, 167)}.{randint(60, 167)}.{randint(60, 167)}"


def random_dns() -> str:
    return choice(['cel_mai_bun_dns.com', 'balunga.io',
                   'nu_este_vina_noastra.dk', 'retele_de_calculatoare.ro', 'cat_este_ceasul.fr'])


def generare_packet(packet: Packet, dhcp_type: MessageType) -> Optional[Packet]:
    packet.dhcp_message_type = dhcp_type
    packet.opcode = Opcodes.REPLY
    for optiune in packet.get_server_options():
        if optiune == 1:
            packet.subnet_mask = f"{255}.{255}.{240}.{0}"
        elif optiune == 3:
            packet.router = random_ip()
        elif optiune == 6:
            packet.domain_server = random_dns()
        elif optiune == 28:
            packet.broadcast_address = random_ip()
        elif optiune == 51:
            packet.lease_time = randint(8, 18)
        elif optiune == 58:
            packet.renewal_time = packet.lease_time // 2 if packet.lease_time else randint(4, 9)

    if packet.address_request is None:
        packet.your_ip_address = random_ip()
        return packet
    else:
        decizie = randint(0, 1)
        print("decizie:", decizie)
        if decizie == 1:
            packet.your_ip_address = packet.address_request
            return packet
        else:
            return None


def run_server():

    while True:
        # asteptare dicover
        data = SERVER_SOCKET.recv(1000)
        packet = Packet(data)
        if packet.dhcp_message_type == MessageType.DISCOVER:
            # construire offer
            packet = generare_packet(packet, MessageType.OFFER)

            # trimitere offer
            if packet is not None:
                SERVER_SOCKET.sendto(packet.encode(), SERVER_BROADCAST_ADDR)

                # primire req
                packet_request = Packet(SERVER_SOCKET.recv(1024))

                # construire ack
                packet_request.opcode = Opcodes.REPLY
                packet_request.dhcp_message_type = MessageType.ACK

                # trimitere ack
                SERVER_SOCKET.sendto(packet_request.encode(), SERVER_BROADCAST_ADDR)
        elif packet.dhcp_message_type == MessageType.REQUEST:
            # construire ack
            packet = generare_packet(packet, MessageType.ACK)

            # trimitere ack
            if packet is not None:
                SERVER_SOCKET.sendto(packet.encode(), SERVER_BROADCAST_ADDR)
        elif packet.dhcp_message_type == MessageType.RELEASE:
            print("eliberat datele")


if __name__ == "__main__":
    run_server()
