from __future__ import annotations
from typing import Optional, List
from Commons.bytes_to_data import BytesToData
from Dhcp.client_options import ClientOptions
from Commons.data_to_bytes import DataToBytes
from Dhcp.opcodes import Opcodes
from Dhcp.server_options import ServerOptions
from Dhcp.message_type import MessageType
from Commons.computer import Computer
from random import randrange


class Packet:
    def __init__(self, packet=None):
        """
        :param packet: A packet from which to copy contents
        """

        self.opcode: Opcodes = Opcodes(BytesToData.bytes_to_int(packet[0:1])) if packet else Opcodes.REQUEST
        self.hardware_type: int = BytesToData.bytes_to_int(packet[1:2]) if packet else 1
        self.hardware_address_length: int = BytesToData.bytes_to_int(packet[2:3]) if packet else 6
        self.hops: int = BytesToData.bytes_to_int(packet[3:4]) if packet else 0
        self.transaction_id: int = BytesToData.bytes_to_hex(packet[4:8]) if packet else randrange(1, 100000)
        self.seconds_elapsed: int = BytesToData.bytes_to_int(packet[8:10]) if packet else 0
        self.boot_flags: int = BytesToData.bytes_to_int(packet[10:12]) if packet else (8 << 12)
        self.client_ip_address: str = BytesToData.bytes_to_ip(packet[12:16]) if packet else '0.0.0.0'
        self.your_ip_address: str = BytesToData.bytes_to_ip(packet[16:20]) if packet else '0.0.0.0'
        self.server_ip_address: str = BytesToData.bytes_to_ip(packet[20:24]) if packet else '0.0.0.0'
        self.gateway_ip_address: str = BytesToData.bytes_to_ip(packet[24:28]) if packet else '0.0.0.0'
        self.client_hardware_address: str = BytesToData.bytes_to_mac(packet[28:34]) if packet else Computer.get_mac()
        self.server_name: str = BytesToData.bytes_to_str(packet[34:108]) if packet else ''
        self.boot_filename: str = BytesToData.bytes_to_str(packet[108:236]) if packet else ''
        self.magic_cookie: int = BytesToData.bytes_to_hex(packet[236:240]) if packet else \
            int.from_bytes(b'\x63\x82\x53\x63', byteorder='big')

        # options
        self.server_options: Optional[List[ServerOptions]] = None
        self.host_name: Optional[str] = None
        self.address_request: Optional[str] = None
        self.dhcp_message_type: Optional[MessageType] = None
        self.client_id: Optional[str] = None

        self.subnet_mask: Optional[str] = None
        self.router: Optional[str] = None
        self.domain_server: Optional[str] = None
        self.broadcast_address: Optional[str] = None
        self.lease_time: Optional[int] = None
        self.renewal_time: Optional[int] = None

        if packet:
            self.set_options_from_bytes(packet)

    def set_options_from_bytes(self, packet: bytes):
        """Set to the current packet the options from the param packet

        :param packet: The packet from which to copy the options
        """
        options_section = packet[240:]
        index = 0
        options_dict = {}

        while True:
            option_code = options_section[index]
            if option_code == 255:
                break
            option_size = options_section[index + 1]
            option_body = options_section[index + 2:index + 2 + option_size]
            options_dict[option_code] = option_body
            index += 2 + option_size

        for x in options_dict:
            if options_dict[x] is not None:
                if x == 1:
                    self.subnet_mask = BytesToData.bytes_to_ip(options_dict[x])
                elif x == 3:
                    self.router = BytesToData.bytes_to_ip(options_dict[x])
                elif x == 6:
                    self.domain_server = BytesToData.bytes_to_ip(options_dict[x])
                elif x == 28:
                    self.broadcast_address = BytesToData.bytes_to_ip(options_dict[x])
                elif x == 51:
                    self.lease_time = BytesToData.bytes_to_int(options_dict[x])
                elif x == 58:
                    self.renewal_time = BytesToData.bytes_to_int(options_dict[x])
                elif x == 0:
                    pass
                elif x == 12:
                    self.host_name = BytesToData.bytes_to_str(options_dict[x])
                elif x == 50:
                    self.address_request = BytesToData.bytes_to_ip(options_dict[x])
                elif x == 53:
                    self.dhcp_message_type = BytesToData.bytes_to_int(options_dict[x])
                elif x == 61:
                    self.client_id = BytesToData.bytes_to_str(options_dict[x])

    def encode(self) -> bytes:
        """Encodes the current packet

        :return: The packet in byte form.
        """
        encoded_packet = b''
        encoded_packet += DataToBytes.int_to_bytes(self.opcode)
        encoded_packet += DataToBytes.int_to_bytes(self.hardware_type)
        encoded_packet += DataToBytes.int_to_bytes(self.hardware_address_length)
        encoded_packet += DataToBytes.int_to_bytes(self.hops)
        encoded_packet += DataToBytes.hex_to_bytes(self.transaction_id)
        encoded_packet += DataToBytes.int_to_bytes(self.seconds_elapsed, 2)
        encoded_packet += DataToBytes.int_to_bytes(self.boot_flags, 2)
        encoded_packet += DataToBytes.ip_to_bytes(self.client_ip_address)
        encoded_packet += DataToBytes.ip_to_bytes(self.your_ip_address)
        encoded_packet += DataToBytes.ip_to_bytes(self.server_ip_address)
        encoded_packet += DataToBytes.ip_to_bytes(self.gateway_ip_address)
        encoded_packet += DataToBytes.mac_to_bytes(self.client_hardware_address, 16)
        encoded_packet += DataToBytes.str_to_bytes(self.server_name, 64)
        encoded_packet += DataToBytes.str_to_bytes(self.boot_filename, 128)
        encoded_packet += DataToBytes.hex_to_bytes(self.magic_cookie, 4)

        if self.server_options and len(self.server_options) > 0:
            encoded_packet += DataToBytes.int_to_bytes(55, 1)
            encoded_packet += DataToBytes.int_to_bytes(len(self.server_options))
            for option in self.server_options:
                encoded_packet += DataToBytes.int_to_bytes(option.value)

        if self.host_name:
            encoded_packet += DataToBytes.int_to_bytes(ClientOptions.HOST_NAME.value) + \
                              DataToBytes.int_to_bytes(len(self.host_name)) + \
                              DataToBytes.str_to_bytes(self.host_name, len(self.host_name))

        if self.address_request:
            encoded_packet += DataToBytes.int_to_bytes(ClientOptions.ADDRESS_REQUEST.value) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.ip_to_bytes(self.address_request)

        if self.dhcp_message_type:
            encoded_packet += DataToBytes.int_to_bytes(ClientOptions.DHCP_MESSAGE_TYPE.value) + \
                              DataToBytes.int_to_bytes(1) + \
                              DataToBytes.int_to_bytes(self.dhcp_message_type)

        if self.client_id:
            encoded_packet += DataToBytes.int_to_bytes(ClientOptions.CLIENT_ID.value) + \
                              DataToBytes.int_to_bytes(len(self.client_id)) + \
                              DataToBytes.str_to_bytes(self.client_id, len(self.client_id))

        if self.subnet_mask:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.SUBNET_MASK) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.ip_to_bytes(self.subnet_mask)

        if self.router:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.ROUTER) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.ip_to_bytes(self.router)

        if self.domain_server:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.DOMAIN_SERVER) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.ip_to_bytes(self.domain_server)

        if self.broadcast_address:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.BROADCAST_ADDRESS) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.ip_to_bytes(self.broadcast_address)

        if self.lease_time:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.LEASE_TIME) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.int_to_bytes(self.lease_time, 4)

        if self.renewal_time:
            encoded_packet += DataToBytes.int_to_bytes(ServerOptions.RENEWAL_TIME) + \
                              DataToBytes.int_to_bytes(4) + \
                              DataToBytes.int_to_bytes(self.renewal_time, 4)

        encoded_packet += DataToBytes.int_to_bytes(255, 1)
        return encoded_packet

    @staticmethod
    def make_request_packet(offer_packet: Packet) -> Optional[Packet]:
        """Transforms an offer packet to a request packet

        :param offer_packet: The packet which will be transformed
        :return: Request packet or None
        """
        if offer_packet.opcode == Opcodes.REPLY and offer_packet.dhcp_message_type == MessageType.OFFER:
            offer_packet.opcode = Opcodes.REQUEST
            offer_packet.dhcp_message_type = MessageType.REQUEST
            offer_packet.address_request = offer_packet.your_ip_address
            offer_packet.your_ip_address = '0.0.0.0'
            return offer_packet
        else:
            return None

    def get_renewal_time(self) -> Optional[int]:
        """
        :return: renewal time in seconds
        """
        return self.renewal_time if self.renewal_time else self.lease_time//2 if self.lease_time else None

    def __str__(self):
        return f"""
        opcode: {self.opcode}
        hardware_type: {self.hardware_type}
        hardware_address_length: {self.hardware_address_length}
        hops: {self.hops}
        transaction_id: {self.transaction_id}
        seconds_elapsed: {self.seconds_elapsed}
        boot_flags: {self.boot_flags}
        client_ip_address: {self.client_ip_address}
        your_ip_address: {self.your_ip_address}
        server_ip_address: {self.server_ip_address}
        gateway_ip_address: {self.gateway_ip_address}
        client_hardware_address: {self.client_hardware_address}
        server_name: {self.server_name}
        boot_filename: {self.boot_filename}
        OPTIONS:\n
        host_name: {self.host_name}
        address_request: {self.address_request}
        dhcp_message_type: {self.dhcp_message_type}
        client: {self.client_id}
        subnet_mask: {self.subnet_mask}
        router: {self.router}
        dns: {self.domain_server}
        broadcast_addr: {self.broadcast_address}
        lease: {self.lease_time}
        renewal: {self.renewal_time}
        option55: {self.server_options}
        """
