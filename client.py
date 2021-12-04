from DHCP_Packet import *
from select import select

SOURCE_PORT = 68
DESTINATION_PORT = 67
SOURCE_ADDR = ("", SOURCE_PORT)
DESTINATIN_ADDR = ('<broadcast>', DESTINATION_PORT)


if __name__ == "__main__":

    # initializare socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SOURCE_ADDR)

    # construire packet DHCP Discover
    packet = Packet(requested_options=[Optiuni_request.SUBNET_MASK, Optiuni_request.DOMAIN_SERVER])
    packet.opcode = Opcodes.REQUEST
    packet.host_name = "salut"
    packet.dhcp_message_type = Tip_Mesaj.DISCOVER
    packet.boot_flags = 1
    packet_bytes = packet.pregateste_packetul()

    # trimitere DISCOVER
    print("Trimitere discover")
    sock.sendto(packet_bytes, DESTINATIN_ADDR)

    # primire mesaj OFFER
    putem_citi, _, _ = select([sock], [], [], 5)
    packet_2 = Packet(sock.recv(1024)) if putem_citi else None

    # verificare si trimitere request
    if packet_2 and packet_2.dhcp_message_type == Tip_Mesaj.OFFER:
        print("Mesaj offer primit")
        packet_2.opcode = Opcodes.REQUEST
        packet_2.dhcp_message_type = Tip_Mesaj.REQUEST
        sock.sendto(packet_2.pregateste_packetul(), DESTINATIN_ADDR)

        # asteptare packet ack
        putem_citi, _, _ = select([sock], [], [], 5)
        packet_ack = Packet(sock.recv(1024)) if putem_citi else None

        # afisare rezultate
        if packet_ack and packet_ack.dhcp_message_type == Tip_Mesaj.ACK:
            print(packet_ack)


