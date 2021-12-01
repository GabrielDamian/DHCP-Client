import socket

server = ''
port = 8080
addr = (server, port)

if __name__ == "__main__":
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(addr)

    print("Server is listening")
    while True:
        data = listener.recv(1000)
        print(data)
        
        
        
#Todos:
#Broadcast care asculta pentru DHCP DISCOVER => Alege daca face sau nu o oferta in functie de resursele pe care le are disponibile
#Socket pentru DHCPREQUEST 
#Socket pentru DHCPACK 
