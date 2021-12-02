import socket
import threading
import time
from DHCP_Packet import Packet,Optiuni,Optiuni_request,BytesToData

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

    #construire packet dhcprequest
    packet = Packet(requested_options=[Optiuni_request.SUBNET_MASK, Optiuni_request.DOMAIN_SERVER])
    packet.host_name = "salut"

    packet_bytes = packet.pregateste_packetul()
    print("verificare:",packet_bytes[240])

    #trimitere DHCPRequest
    sock.sendto(packet_bytes, ADDR)

    # while True:
    #     sock.sendto(b"Hello",('<broadcast>',PORT))
    #     print("Trimis Hello")
    #     time.sleep(5)
        
        
        
 #Todos:
 #Functie care trimite DHCP DISCOVER
 #Socket pentru primirea ofertei de la server (sau servere) //DHCP OFFER
 #Functie pentru DHCPREQUEST catre serverul selectat
 #Socket care primeste DHCPACK pentru inchirierea datelor
 #Functie care ruleaza periodic pentru reinnoirea contractului
 #Functie pentru deconectare de la server
 
 
 #Structura mesaje in fisier separat (urmand sa fie utilizate atat de client cat si de server)
 
 