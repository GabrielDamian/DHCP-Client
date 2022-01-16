from random import randrange

from DHCP_Client.bytes_to_data import BytesToData
from DHCP_Client.client_options import ClientOptions
from DHCP_Client.data_to_bytes import DataToBytes
from DHCP_Client.opcodes import Opcodes
from DHCP_Client.server_options import ServerOptions


class Packet:
    def __init__(self, packet=None, requested_options: list = ()):
        self.opcode = Opcodes(BytesToData.bytes_to_int(packet[0:1])) if packet else Opcodes.NONE
        self.hardware_type = BytesToData.bytes_to_int(packet[1:2]) if packet else 1  # 1 - Ethernet
        self.hardware_address_length = BytesToData.bytes_to_int(packet[2:3]) if packet else 6
        self.hops = BytesToData.bytes_to_int(packet[3:4]) if packet else 0
        self.transaction_id = BytesToData.bytes_to_hex(packet[4:8]) if packet else randrange(0x100000)
        self.seconds_elapsed = BytesToData.bytes_to_int(packet[8:10]) if packet else 0
        self.boot_flags = BytesToData.bytes_to_int(packet[10:12]) if packet else 0
        self.client_ip_address = BytesToData.bytes_to_ip(packet[12:16]) if packet else '0.0.0.0'
        self.your_ip_address = BytesToData.bytes_to_ip(packet[16:20]) if packet else '0.0.0.0'
        self.server_ip_address = BytesToData.bytes_to_ip(packet[20:24]) if packet else '0.0.0.0'
        self.gateway_ip_address = BytesToData.bytes_to_ip(packet[24:28]) if packet else '0.0.0.0'
        self.client_hardware_address = BytesToData.bytes_to_mac(packet[28:34]) if packet else '1A:2B:3C:3C:C4:EF'
        self.server_name = BytesToData.bytes_to_str(packet[34:108]) if packet else ''
        self.boot_filename = BytesToData.bytes_to_str(packet[108:236]) if packet else ''
        self.magic_cookie = BytesToData.bytes_to_hex(packet[236:240]) if packet else int.from_bytes(b'\x63\x82\x53\x63',
                                                                                                    byteorder='big')
        self.host_name = None
        self.address_request = None
        self.dhcp_message_type = None
        self.client_id = None

        # optiuni server
        self.subnet_mask = None
        self.router = None
        self.domain_server = None
        self.broadcast_address = None
        self.lease_time = None
        self.renewal_time = None

        # requested parameters
        self.option55 = None

        self.overwrite_server_options(requested_options)

        # initializare cu un packet
        if packet:
            self.set_options_from_bytes(packet[240:])

    def overwrite_server_options(self, requested_options):
        if len(requested_options) > 0:
            self.option55 = DataToBytes.int_to_bytes(55, 1)
            self.option55 += DataToBytes.int_to_bytes(len(requested_options))
            for option in requested_options:
                self.option55 += DataToBytes.int_to_bytes(option.value)

    def get_server_options(self) -> list:
        optiuni = []
        for byte in self.option55[2:]:
            optiuni.append(int(byte))
        return optiuni

    def set_options_from_bytes(self, packet: bytes):
        index = 0
        optiunu_dic = {}
        while index < len(packet) - 1:
            op_code = packet[index]
            op_size = packet[index + 1]
            op = packet[index + 2:index + 2 + op_size]
            op_55_arr = []
            if op_code == 55:
                for x in op:
                    op_55_arr.append(x)

            if op_code == 55:
                optiunu_dic[55] = op_55_arr
            else:
                optiunu_dic[op_code] = op

            index += 1 + 1 + op_size

        for x in optiunu_dic:
            if optiunu_dic[x] is not None:
                if x == 55 and len(optiunu_dic[55]) > 0:
                    self.option55 = DataToBytes.int_to_bytes(55) + DataToBytes.int_to_bytes(len(optiunu_dic[55]))
                    for optiune in optiunu_dic[55]:
                        self.option55 += DataToBytes.int_to_bytes(optiune)
                if x == 1:
                    self.subnet_mask = BytesToData.bytes_to_ip(optiunu_dic[x])
                if x == 3:
                    self.router = BytesToData.bytes_to_ip(optiunu_dic[x])
                if x == 6:
                    self.domain_server = BytesToData.bytes_to_str(optiunu_dic[x])
                if x == 28:
                    self.broadcast_address = BytesToData.bytes_to_ip(optiunu_dic[x])
                if x == 51:
                    self.lease_time = BytesToData.bytes_to_int(optiunu_dic[x])
                if x == 58:
                    self.renewal_time = BytesToData.bytes_to_int(optiunu_dic[x])
                if x == 0:
                    pass
                if x == 12:
                    self.host_name = BytesToData.bytes_to_str(optiunu_dic[x])
                if x == 50:
                    self.address_request = BytesToData.bytes_to_ip(optiunu_dic[x])
                if x == 53:
                    self.dhcp_message_type = BytesToData.bytes_to_int(optiunu_dic[x])
                if x == 61:
                    self.client_id = BytesToData.bytes_to_str(optiunu_dic[x])

    def encode(self) -> bytes:
        packet_pregatit = b''
        packet_pregatit += DataToBytes.int_to_bytes(self.opcode)
        packet_pregatit += DataToBytes.int_to_bytes(self.hardware_type)
        packet_pregatit += DataToBytes.int_to_bytes(self.hardware_address_length)
        packet_pregatit += DataToBytes.int_to_bytes(self.hops)
        packet_pregatit += DataToBytes.hex_to_bytes(self.transaction_id)
        packet_pregatit += DataToBytes.int_to_bytes(self.seconds_elapsed, 2)
        packet_pregatit += DataToBytes.int_to_bytes(self.boot_flags, 2)
        packet_pregatit += DataToBytes.ip_to_bytes(self.client_ip_address)
        packet_pregatit += DataToBytes.ip_to_bytes(self.your_ip_address)
        packet_pregatit += DataToBytes.ip_to_bytes(self.server_ip_address)
        packet_pregatit += DataToBytes.ip_to_bytes(self.gateway_ip_address)
        packet_pregatit += DataToBytes.mac_to_bytes(self.client_hardware_address, 16)
        packet_pregatit += DataToBytes.str_to_bytes(self.server_name, 64)
        packet_pregatit += DataToBytes.str_to_bytes(self.boot_filename, 128)
        packet_pregatit += DataToBytes.hex_to_bytes(self.magic_cookie, 4)

        if self.option55:
            packet_pregatit += self.option55

        if self.host_name:
            packet_pregatit += DataToBytes.int_to_bytes(ClientOptions.HOST_NAME.value) + \
                               DataToBytes.int_to_bytes(len(self.host_name)) + \
                               DataToBytes.str_to_bytes(self.host_name, len(self.host_name))

        if self.address_request:
            packet_pregatit += DataToBytes.int_to_bytes(ClientOptions.ADDRESS_REQUEST.value) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.ip_to_bytes(self.address_request)

        if self.dhcp_message_type:
            packet_pregatit += DataToBytes.int_to_bytes(ClientOptions.DHCP_MESSAGE_TYPE.value) + \
                               DataToBytes.int_to_bytes(1) + \
                               DataToBytes.int_to_bytes(self.dhcp_message_type)

        if self.client_id:
            packet_pregatit += DataToBytes.int_to_bytes(ClientOptions.CLIENT_ID.value) + \
                               DataToBytes.int_to_bytes(len(self.client_id)) + \
                               DataToBytes.str_to_bytes(self.client_id, len(self.client_id))

        if self.subnet_mask:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.SUBNET_MASK) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.ip_to_bytes(self.subnet_mask)

        if self.router:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.ROUTER) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.ip_to_bytes(self.router)

        if self.domain_server:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.DOMAIN_SERVER) + \
                               DataToBytes.int_to_bytes(len(self.domain_server)) + \
                               DataToBytes.str_to_bytes(self.domain_server, len(self.domain_server))

        if self.broadcast_address:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.BROADCAST_ADRESS) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.ip_to_bytes(self.broadcast_address)

        if self.lease_time:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.LEASE_TIME) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.int_to_bytes(self.lease_time, 4)

        if self.renewal_time:
            packet_pregatit += DataToBytes.int_to_bytes(ServerOptions.RENEWAL_TIME) + \
                               DataToBytes.int_to_bytes(4) + \
                               DataToBytes.int_to_bytes(self.renewal_time, 4)

        packet_pregatit += DataToBytes.int_to_bytes(255, 1)
        return packet_pregatit

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
        OPTIUNI:\n
        host_name: {self.host_name}
        address_request: {self.address_request}
        dhcp_message_type: {self.dhcp_message_type}
        client: {self.client_id}
        subnet_mask: {self.subnet_mask}
        router: {self.router}
        dns: {self.domain_server}
        broadcard_addr: {self.broadcast_address}
        lease: {self.lease_time}
        renewal: {self.renewal_time}
        op55: {self.option55}
        """
