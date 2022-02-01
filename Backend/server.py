from select import select
from Dhcp.packet import Packet
from Dhcp.opcodes import Opcodes
from Dhcp.message_type import MessageType
from socket import socket, AF_INET, SOL_SOCKET, SOCK_DGRAM, SO_BROADCAST, SO_REUSEADDR
from Commons.computer import Computer
from Dhcp.address_table import AddressTable
from typing import Optional
import ipaddress
from datetime import datetime, timedelta
from threading import Thread


class Server:
    def __init__(self, network_ip_address: str, mask: str, router: str, dns: str, lease_time: int, renewal_time: int):
        self._bind_address = (Computer.get_wifi_ip_address(), 67)
        self._broadcast_address = ('255.255.255.255', 68)
        self._network_ip_address = network_ip_address
        self._mask = mask
        self._address_table: Optional[AddressTable] = None
        self.router = router
        self.dns = dns
        self.lease_time = lease_time
        self.renewal_time = renewal_time
        self._last_selected_ip_address: Optional[ipaddress.IPv4Address] = None
        self._stop_request = False

        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind(self._bind_address)

    def stop(self):
        """Stop the server and clear the address table"""
        self._stop_request = True
        self._address_table.clear()

    def _send_message(self, message: Packet):
        """
        Broadcast a dhcp packet
        :param message: Packet that will be sent
        """
        self._socket.sendto(message.encode(), self._broadcast_address)

    def _listen_packets(self):
        """Listen for DHCP messages and handle them"""
        while not self._stop_request:
            message_received, _, _ = select([self._socket], [], [], 60)
            packet = Packet(self._socket.recv(1024)) if message_received else None
            if packet is None:
                return
            elif packet.opcode == Opcodes.REQUEST and packet.dhcp_message_type == MessageType.DISCOVER:
                Thread(target=self._handle_discover, args=(packet,)).start()
            elif packet.opcode == Opcodes.REQUEST and packet.dhcp_message_type == MessageType.REQUEST:
                Thread(target=self._handle_request, args=(packet,)).start()
            elif packet.opcode == Opcodes.REQUEST and packet.dhcp_message_type == MessageType.RELEASE:
                Thread(target=self._handle_release, args=(packet,)).start()
            else:
                raise Exception("Not recognised message")

    def _handle_discover(self, discover_message: Packet):
        """
        Takes a discover packet, processes it into offer and sends it
        :param discover_message: The discover packet
        """
        self._last_selected_ip_address = self._address_table.get_unallocated_address()
        discover_message.your_ip_address = str(self._last_selected_ip_address)
        discover_message.subnet_mask = self._address_table.get_subnet_mask()
        discover_message.router = self.router
        discover_message.domain_server = self.dns
        discover_message.lease_time = self.lease_time
        discover_message.renewal_time = self.renewal_time
        discover_message.dhcp_message_type = MessageType.OFFER
        discover_message.opcode = Opcodes.REPLY

        self._send_message(discover_message)

    def _handle_request(self, request_packet: Packet):
        """
        Takes a request packet, processes it into ack and sends it
        :param request_packet: The request packet
        """
        request_packet.your_ip_address = str(self._last_selected_ip_address)
        request_packet.dhcp_message_type = MessageType.ACK
        request_packet.opcode = Opcodes.REPLY
        self._send_message(request_packet)

        self._address_table.give_address(self._last_selected_ip_address, request_packet.client_hardware_address,
                                         request_packet.client_id,
                                         datetime.now() + timedelta(seconds=int(self.lease_time)))
        print(self._address_table)

    def _handle_release(self, release_packet: Packet):
        """
        Marks the ip address from the packet as not used
        :param release_packet: DHCP Release packet
        """
        self._address_table.release_address(ipaddress.IPv4Address(release_packet.address_request))
        print(self._address_table)

    def start(self):
        """Start the server"""
        ip = f'{self._network_ip_address}{self._mask}'
        network_ip = ipaddress.ip_network(address=ip, strict=False)
        self._address_table = AddressTable(network_ip)

        Thread(target=self._listen_packets).start()

    def __str__(self):
        return str(self._address_table)


if __name__ == "__main__":
    Server(network_ip_address='10.20.30.40', mask='/29',
           router='1.2.3.4', dns='4.3.2.1', lease_time=120, renewal_time=60).start()
