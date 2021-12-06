import time

from DHCP_Packet import *

BIND_ADDRESS = ('', 67)
BROADCAST_ADDR = ('<broadcast>', 68)

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
            packet.dhcp_message_type = Tip_Mesaj.OFFER
            packet.opcode = Opcodes.REPLY
            packet.host_name = "setat de server"
            packet.domain_server = "salut_gg.io"
            packet.your_ip_address = '1.1.1.1'
            packet.lease_time = 100
            packet.renewal_time = 5

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
            print('Damian a vrut asta')
            # construire ack
            packet.opcode = Opcodes.REPLY
            packet.lease_time = 100
            packet.renewal_time = 7
            packet.dhcp_message_type = Tip_Mesaj.ACK
            packet.your_ip_address= '2.2.2.2'

            # trimitere ack
            time.sleep(2)
            listener.sendto(packet.pregateste_packetul(), BROADCAST_ADDR)
