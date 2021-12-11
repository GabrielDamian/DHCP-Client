from random import randint, choice
from DHCP_Client.DHCP_Packet import Packet, Tip_Mesaj, Opcodes
from DHCP_Client import SERVER_SOCKET, SERVER_BROADCAST_ADDR
from typing import Optional


def random_ip() -> str:
    return f"{randint(60, 167)}.{randint(60, 167)}.{randint(60, 167)}.{randint(60, 167)}"


def random_dns() -> str:
    return choice(['cel_mai_bun_dns.com', 'balunga.io',
                   'nu_este_vina_noastra.dk', 'retele_de_calculatoare.ro', 'cat_este_ceasul.fr'])


def generare_packet(packet: Packet, dhcp_type: Tip_Mesaj) -> Optional[Packet]:
    packet.dhcp_message_type = dhcp_type
    packet.opcode = Opcodes.REPLY
    for optiune in packet.extragere_din_op55():
        if optiune == 1:
            packet.subnet_mask = f"{255}.{255}.{240}.{0}"
        if optiune == 3:
            packet.router = random_ip()
        if optiune == 6:
            packet.domain_server = random_dns()
        if optiune == 28:
            packet.broadcast_address = random_ip()
        if optiune == 51:
            packet.lease_time = randint(8, 18)
        if optiune == 58:
            packet.renewal_time = packet.lease_time // 2 if packet.lease_time else randint(4, 9)

    if packet.address_request == '0.0.0.0':
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
        if packet.dhcp_message_type == Tip_Mesaj.DISCOVER:
            # construire offer
            packet = generare_packet(packet, Tip_Mesaj.OFFER)

            # trimitere offer
            if packet is not None:
                SERVER_SOCKET.sendto(packet.pregateste_packetul(), SERVER_BROADCAST_ADDR)

                # primire req
                packet_request = Packet(SERVER_SOCKET.recv(1024))

                # construire ack
                packet_request.opcode = Opcodes.REPLY
                packet_request.dhcp_message_type = Tip_Mesaj.ACK

                # trimitere ack
                SERVER_SOCKET.sendto(packet_request.pregateste_packetul(), SERVER_BROADCAST_ADDR)
        elif packet.dhcp_message_type == Tip_Mesaj.REQUEST:
            # construire ack
            packet = generare_packet(packet, Tip_Mesaj.ACK)

            # trimitere ack
            if packet is not None:
                SERVER_SOCKET.sendto(packet.pregateste_packetul(), SERVER_BROADCAST_ADDR)
        elif packet.dhcp_message_type == Tip_Mesaj.RELEASE:
            print("eliberat datele")


if __name__ == "__main__":
    run_server()
