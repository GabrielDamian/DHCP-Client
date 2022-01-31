from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR


def get_ip() -> str:
    """
    :return: The IP address of wi-fi interface
    """
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))  # the address does not matter
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


WIFI_IP = get_ip()

SERVER_BIND_ADDRESS = (WIFI_IP, 67)
SERVER_BROADCAST_ADDRESS = ('255.255.255.255', 68)
CLIENT_SOURCE_ADDRESS = (WIFI_IP, 68)
CLIENT_DESTINATION_ADDRESS = ('255.255.255.255', 67)

CLIENT_SOCKET = socket(AF_INET, SOCK_DGRAM)
CLIENT_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
CLIENT_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
CLIENT_SOCKET.bind(CLIENT_SOURCE_ADDRESS)

SERVER_SOCKET = socket(AF_INET, SOCK_DGRAM)
SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER_SOCKET.bind(SERVER_BIND_ADDRESS)

SUBNET_MASKS = [f'/{i}' for i in range(0, 33)]
NETWORK_SIZES = {value: 2**(len(SUBNET_MASKS)-1-index) for index, value in enumerate(SUBNET_MASKS)}
