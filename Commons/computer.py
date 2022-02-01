from uuid import getnode
from socket import socket, AF_INET, SOCK_DGRAM

class Computer:
    @staticmethod
    def get_mac() -> str:
        """
        :return: The MAC address of the computer
        """
        return ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))

    @staticmethod
    def get_wifi_ip_address() -> str:
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