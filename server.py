import time
from random import randint, choice
from DHCP_Packet import *

BIND_ADDRESS = ('', 67)
BROADCAST_ADDR = ('<broadcast>', 68)


def random_ip():
    return f"{randint(60,167)}.{randint(60,167)}.{randint(60,167)}.{randint(60,167)}"


def random_dns():
    return choice(['cel_mai_bun_dns.com', 'balunga.io', 'nu_este_vina_noastra.dk', 'retele_de_calculatoare.ro', 'cat_este_ceasul.fr'])

def generare_packet(packet:Packet , dhcp_type: Tip_Mesaj) -> Packet:
    packet = Packet(data)
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
        print("decizie:",decizie)
        if decizie == 1:
            packet.your_ip_address = packet.address_request
            return packet
        else:
            return None


if __name__ == "__main__":
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(BIND_ADDRESS)

    while True:
        print("Server is listening")
        # asteptare dicover
        data = listener.recv(1000)
        packet = Packet(data)
        if packet.dhcp_message_type == Tip_Mesaj.DISCOVER:
            # construire offer
            packet = generare_packet(packet, Tip_Mesaj.OFFER)

            # trimitere offer
            time.sleep(2)
            listener.sendto(packet.pregateste_packetul(), BROADCAST_ADDR)

            # primire req
            packet_request = Packet(listener.recv(1024))

            # construire ack
            packet_request.opcode = Opcodes.REPLY
            packet_request.dhcp_message_type = Tip_Mesaj.ACK

            # trimitere ack
            time.sleep(2)
            listener.sendto(packet_request.pregateste_packetul(), BROADCAST_ADDR)
        elif packet.dhcp_message_type == Tip_Mesaj.REQUEST:
            # construire ack
            packet = generare_packet(packet, Tip_Mesaj.ACK)
            #decid daca vr sa ii raspund (daca am sau nu resursele necesare), decizie random aici (in mod normal ar trebui verificate listele de ocupare a resurselor)

            if packet != None:
                listener.sendto(packet.pregateste_packetul(), BROADCAST_ADDR)
            else:
                pass
            # trimitere ack
            time.sleep(2)


        elif packet.dhcp_message_type == Tip_Mesaj.RELEASE:
            print("eliberat datele")
