from Dhcp.packet import Packet
from Commons.computer import Computer
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR
from typing import Optional, List, Union
from Dhcp.server_options import ServerOptions
from Dhcp.opcodes import Opcodes
from Dhcp.message_type import MessageType
from Commons.receivers import Receivers
from queue import Queue
from Commons.timer import Timer


class Client:
    def __init__(self, server_options: Optional[List[ServerOptions]] = None,
                 host_name: Optional[str] = None, address_request: Optional[str] = None, client_id: Optional[str] = None,
                 mac: Optional[str] = None, client_ip_address: Optional[str] = None, logging_queue: Queue = Queue()):
        self.server_options = server_options
        self.host_name = host_name
        self.address_request = address_request
        self.client_id = client_id
        self.mac = mac
        self.client_ip_address = client_ip_address
        self._logging_queue = logging_queue
        self._source_address = (Computer.get_wifi_ip_address(), 68)
        self._broadcast_address = ('255.255.255.255', 67)
        self._last_request_packet: Optional[Packet] = None
        self._timer: Optional[Timer] = None

        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind(self._source_address)

    def connect(self):
        self._log("Sending discover...")
        self._send_discover()

        offer_packet = Receivers.offer_receiver(self._socket, 10)
        if offer_packet is None:
            self._no_response_from_server()
            return
        self._log("Offer received...")

        self._last_request_packet = Packet.make_request_packet(offer_packet=offer_packet)
        self._log("Sending request...")
        self._send_message(self._last_request_packet)

        ack_packet = Receivers.ack_receiver(self._socket, 10)
        if ack_packet is None:
            self._no_response_from_server()
            return
        self._log("Ack received...")

        self._log(str(ack_packet))
        self._log(ack_packet.encode())

        self._timer = Timer(ack_packet.get_renewal_time(), self.reconnect)
        self._timer.start()

    def reconnect(self):
        self._timer.cancel()
        self._log("Sending request...")
        self._send_message(self._last_request_packet)

        packet_ack = Receivers.ack_receiver(self._socket)
        if packet_ack is None:
            self._no_response_from_server()
            return

        self._log("Ack received...")
        self._log(packet_ack.encode())
        if packet_ack.get_renewal_time():
            self._timer = Timer(packet_ack.get_renewal_time(), self.reconnect)
            self._timer.start()

    def disconnect(self):
        if self._timer:
            self._timer.cancel()
        packet_release = self._last_request_packet
        packet_release.dhcp_message_type = MessageType.RELEASE
        packet_release.opcode = Opcodes.REQUEST
        self._send_message(packet_release)
        self._log("Disconnected.")

    def _send_discover(self):
        discover_packet = Packet()
        discover_packet.server_options = self.server_options
        discover_packet.host_name = self.host_name
        discover_packet.address_request = self.address_request
        discover_packet.client_id = self.client_id
        discover_packet.mac = self.mac
        discover_packet.client_ip_address = self.client_ip_address
        discover_packet.opcode = Opcodes.REQUEST
        discover_packet.dhcp_message_type = MessageType.DISCOVER
        self._send_message(discover_packet)

    def _no_response_from_server(self):
        self._log("No response from server.")

    def _log(self, message: Union[str, bytes]):
        self._logging_queue.put(message)

    def _send_message(self, message: Packet):
        """
        Broadcast a dhcp packet
        :param message: Packet that will be sent
        """
        self._socket.sendto(message.encode(), self._broadcast_address)
