import socket
from enum import IntEnum
from random import randrange


class DataToBytes:
    @staticmethod
    def ipToBytes(data: str) -> bytes:
        return socket.inet_aton(data)  # length 4 octeti

    @staticmethod
    def hexToBytes(data, length: int = 4) -> bytes:
        return data.to_bytes(length, 'big')

    @staticmethod
    def intToBytes(data: int, length: int = 1) -> bytes:
        return data.to_bytes(length, 'big')

    @staticmethod
    def macToBytes(data: str, length: int = 6) -> bytes:
        vec = [bytes.fromhex(x).lower() for x in data.split(":")]
        final = b''
        for e in vec:
            final += e
        return final + (length - final.__len__()) * b'\x00'

    @staticmethod
    def strToBytes(data: str, length: int) -> bytes:
        final = str.encode(data)
        return final + (length - len(final)) * b'\x00'


class BytesToData:
    @staticmethod
    def bytesToIp(data: bytes) -> str:
        arr = [int(x) for x in data]
        ip = '.'.join(str(x) for x in arr)
        return str(ip)

    @staticmethod
    def bytesToHex(data: bytes) -> int:
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytesToStr(data: bytes) -> str:
        final = data.decode("utf-8")
        return final.replace('\0', '')

    @staticmethod
    def bytesToInt(data: bytes) -> int:
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytesToMac(data: bytes) -> str:
        rez = ''
        for x in data:
            rez += str(hex(x)[2:]) + ":"
        return rez[:-1]


class Opcodes(IntEnum):
    NONE = 0
    REQUEST = 1
    REPLY = 2


class Tip_Mesaj(IntEnum):
    NONE = 0
    DISCOVER = 1
    OFFER = 2
    REQUEST = 3
    DECLINE = 4
    ACK = 5
    RELEASE = 6


class Optiuni_request(IntEnum):
    SUBNET_MASK = 1
    ROUTER = 3
    DOMAIN_SERVER = 6
    BROADCAST_ADRESS = 28
    LEASE_TIME = 51
    RENEWAL_TIME = 58


class Optiuni(IntEnum):
    PAD = 0
    HOST_NAME = 12
    ADDRESS_REQUEST = 50
    DHCP_MESSAGE_TYPE = 53
    CLIENT_ID = 61
    END = 255


class Packet:
    def __init__(self, packet=None, requested_options: list = ()):
        self.opcode = Opcodes(BytesToData.bytesToInt(packet[0:1])) if packet else Opcodes.NONE
        self.hardware_type = BytesToData.bytesToInt(packet[1:2]) if packet else 1  # 1 - Ethernet
        self.hardware_address_length = BytesToData.bytesToInt(packet[2:3]) if packet else 6
        self.hops = BytesToData.bytesToInt(packet[3:4]) if packet else 0  # noduri intermediare prin care a trecut mesajul
        self.transaction_id = BytesToData.bytesToHex(packet[4:8]) if packet else randrange(0x100000)  # token random de identificare mesaj propriu
        self.seconds_elapsed = BytesToData.bytesToInt(packet[8:10]) if packet else 0  # number of seconds elapsed since a client began an attempt to acquire or renew a lease
        self.boot_flags = BytesToData.bytesToInt(packet[10:12]) if packet else 0
        self.client_ip_address = BytesToData.bytesToIp(packet[12:16]) if packet else '0.0.0.0'
        self.your_ip_address = BytesToData.bytesToIp(packet[16:20]) if packet else '0.0.0.0'
        self.server_ip_address = BytesToData.bytesToIp(packet[20:24]) if packet else '0.0.0.0'
        self.gateway_ip_address = BytesToData.bytesToIp(packet[24:28]) if packet else '0.0.0.0'
        self.client_hardware_address = BytesToData.bytesToMac(packet[28:34]) if packet else '1A:2B:3C:3C:C4:EF'
        self.server_name = BytesToData.bytesToStr(packet[34:108]) if packet else ''
        self.boot_filename = BytesToData.bytesToStr(packet[108:236]) if packet else ''
        self.magic_cookie = BytesToData.bytesToHex(packet[236:240]) if packet else int.from_bytes(b'\x63\x82\x53\x63', byteorder='big')
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
        self.op55 = None

        self.suprascrie_optiuni_55(requested_options)

        # initializare cu un packet
        if packet:
            self.set_optiuni_from_bytes(packet[240:])

    def suprascrie_optiuni_55(self, requested_options):
        if len(requested_options) > 0:
            self.op55 = DataToBytes.intToBytes(55, 1)
            self.op55 += DataToBytes.intToBytes(len(requested_options))
            for option in requested_options:
                self.op55 += DataToBytes.intToBytes(option.value)

    def extragere_din_op55(self) -> list:
        optiuni = []
        for octet in self.op55[2:]:
            optiuni.append(int(octet))
        return optiuni

    def set_optiuni_from_bytes(self, packet: bytes):
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
            if x == 55:
                self.op55 = DataToBytes.intToBytes(55) + DataToBytes.intToBytes(len(optiunu_dic[55]))
                for optiune in optiunu_dic[55]:
                    self.op55 += DataToBytes.intToBytes(optiune)
            if x == 1:
                self.subnet_mask = BytesToData.bytesToIp(optiunu_dic[x])
            if x == 3:
                self.router = BytesToData.bytesToIp(optiunu_dic[x])
            if x == 6:
                self.domain_server = BytesToData.bytesToStr(optiunu_dic[x])
            if x == 28:
                self.broadcast_address = BytesToData.bytesToIp(optiunu_dic[x])
            if x == 51:
                self.lease_time = BytesToData.bytesToInt(optiunu_dic[x])
            if x == 58:
                self.renewal_time = BytesToData.bytesToInt(optiunu_dic[x])
            if x == 0:
                pass
            if x == 12:
                self.host_name = BytesToData.bytesToStr(optiunu_dic[x])
            if x == 50:
                self.address_request = BytesToData.bytesToIp(optiunu_dic[x])
            if x == 53:
                self.dhcp_message_type = BytesToData.bytesToInt(optiunu_dic[x])
            if x == 61:
                self.client_id = BytesToData.bytesToStr(optiunu_dic[x])

    def pregateste_packetul(self) -> bytes:
        packet_pregatit = b''
        packet_pregatit += DataToBytes.intToBytes(self.opcode)
        packet_pregatit += DataToBytes.intToBytes(self.hardware_type)
        packet_pregatit += DataToBytes.intToBytes(self.hardware_address_length)
        packet_pregatit += DataToBytes.intToBytes(self.hops)
        packet_pregatit += DataToBytes.hexToBytes(self.transaction_id)
        packet_pregatit += DataToBytes.intToBytes(self.seconds_elapsed, 2)
        packet_pregatit += DataToBytes.intToBytes(self.boot_flags, 2)
        packet_pregatit += DataToBytes.ipToBytes(self.client_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.your_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.server_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.gateway_ip_address)
        packet_pregatit += DataToBytes.macToBytes(self.client_hardware_address, 16)
        packet_pregatit += DataToBytes.strToBytes(self.server_name, 64)
        packet_pregatit += DataToBytes.strToBytes(self.boot_filename, 128)
        packet_pregatit += DataToBytes.hexToBytes(self.magic_cookie, 4)

        if self.op55:
            packet_pregatit += self.op55

        if self.host_name:
            packet_pregatit += DataToBytes.intToBytes(Optiuni.HOST_NAME.value) + DataToBytes.intToBytes(
                len(self.host_name)) \
                               + DataToBytes.strToBytes(self.host_name, len(self.host_name))
        if self.address_request:
            packet_pregatit += DataToBytes.intToBytes(Optiuni.ADDRESS_REQUEST.value) + DataToBytes.intToBytes(4) \
                               + DataToBytes.ipToBytes(self.address_request)
        if self.dhcp_message_type:
            packet_pregatit += DataToBytes.intToBytes(Optiuni.DHCP_MESSAGE_TYPE.value) + DataToBytes.intToBytes(1) \
                               + DataToBytes.intToBytes(self.dhcp_message_type)
        if self.client_id:
            packet_pregatit += DataToBytes.intToBytes(Optiuni.CLIENT_ID.value) + DataToBytes.intToBytes(
                len(self.client_id)) \
                               + DataToBytes.strToBytes(self.client_id, len(self.client_id))

        if self.subnet_mask:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.SUBNET_MASK) + DataToBytes.intToBytes(4) \
                               + DataToBytes.ipToBytes(self.subnet_mask)

        if self.router:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.ROUTER) + DataToBytes.intToBytes(4) \
                               + DataToBytes.ipToBytes(self.router)

        if self.domain_server:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.DOMAIN_SERVER) + DataToBytes.intToBytes(
                len(self.domain_server)) \
                               + DataToBytes.strToBytes(self.domain_server, len(self.domain_server))

        if self.broadcast_address:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.BROADCAST_ADRESS) + DataToBytes.intToBytes(4) \
                               + DataToBytes.ipToBytes(self.broadcast_address)

        if self.lease_time:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.LEASE_TIME) + DataToBytes.intToBytes(4) \
                               + DataToBytes.intToBytes(self.lease_time, 4)

        if self.renewal_time:
            packet_pregatit += DataToBytes.intToBytes(Optiuni_request.RENEWAL_TIME) + DataToBytes.intToBytes(4) \
                               + DataToBytes.intToBytes(self.renewal_time, 4)

        packet_pregatit += DataToBytes.intToBytes(255, 1)
        return packet_pregatit

    def __str__(self):
        msg: str = f"""
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
        op55: {self.op55}
        """
        return msg