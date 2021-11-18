import socket
import threading
import time

PORT = 8080
ADRESS = ""
ADDR = (ADRESS,PORT)
FORMAT = "utf-8"

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ADRESS, PORT))

    while True:
        sock.sendto(b"Hello",('<broadcast>',PORT))
        print("Trimis Hello")
        time.sleep(5)
        
        
        
 #Todos:
 #Functie care trimite DHCP DISCOVER
 #Socket pentru primirea ofertei de la server (sau servere) //DHCP OFFER
 #Functie pentru DHCPREQUEST catre serverul selectat
 #Socket care primeste DHCPACK pentru inchirierea datelor
 #Functie care ruleaza periodic pentru reinnoirea contractului
 #Functie pentru deconectare de la server
 
 
 #Structura mesaje in fisier separat (urmand sa fie utilizate atat de client cat si de server)
 
 