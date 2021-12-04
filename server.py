from DHCP_Packet import *

server = ''
port = 67
addr = (server, port)
BROADCAST_ADDR = ('<broadcast>',68)
if __name__ == "__main__":
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(addr)

    print("Server is listening")
    # asteptare dicover
    data = listener.recv(1000)

    # construire offer
    packet = Packet(data)
    packet.dhcp_message_type = Tip_Mesaj.OFFER
    packet.opcode = Opcodes.REPLY
    packet.host_name = "setat de server"

    # trimitere offer
    listener.sendto(packet.pregateste_packetul(), BROADCAST_ADDR)

    # primire req
    packet_request = Packet(listener.recv(1024))

    # construire ack
    packet_request.opcode = Opcodes.REPLY
    packet_request.dhcp_message_type = Tip_Mesaj.ACK

    # trimitere ack
    listener.sendto(packet_request.pregateste_packetul(), BROADCAST_ADDR)

