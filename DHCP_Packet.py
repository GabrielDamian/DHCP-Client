import socket
from enum import IntEnum
from random import randrange

class DataToBytes:
    @staticmethod
    def ipToBytes(data: str):
        return socket.inet_aton(data) #length 4 octeti

    @staticmethod
    def hexToBytes(data, length: int = 4):
        return data.to_bytes(length, 'big')

    @staticmethod
    def intToBytes(data: int, length: int = 1):
        return data.to_bytes(length, 'big')

    @staticmethod
    def macToBytes(data: str, length: int = 6):
        vec = [bytes.fromhex(x).lower() for x in data.split(":")]
        final = b''
        for e in vec:
            final += e
        return final + (length - final.__len__()) * b'\x00'

    @staticmethod
    def strToBytes(data: str, length: int):
        final = str.encode(data)
        return final + (length - len(final)) * b'\x00'


class BytesToData:
    @staticmethod
    def bytesToIp(data: bytes):
        arr = [int(x) for x in data]
        ip = '.'.join(str(x) for x in arr)
        return str(ip)

    @staticmethod
    def bytesToHex(data: bytes):
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytesToStr(data: bytes):
        final = data.decode("utf-8")
        return final.replace('\0', '')

    @staticmethod
    def bytesToInt(data: bytes):
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


class Packet:
    def __init__(self, packet=None):
        self.opcode = Opcodes(BytesToData.bytesToInt(packet[0:1])) if packet else Opcodes.NONE
        self.hardware_type = BytesToData.bytesToInt(packet[1:2]) if packet else 1  #1 - Ethernet
        self.hardware_address_length = BytesToData.bytesToInt(packet[2:3]) if packet else 6
        self.hops = BytesToData.bytesToInt(packet[3:4]) if packet else 0 #noduri intermediare prin care a trecut mesajul
        self.transaction_id = BytesToData.bytesToHex(packet[4:8]) if packet else randrange(0x100000000) #token random de identificare mesaj propriu
        self.seconds_elapsed = BytesToData.bytesToInt(packet[8:10]) if packet else 0 #number of seconds elapsed since a client began an attempt to acquire or renew a lease
        self.boot_flags = BytesToData.bytesToHex(packet[10:12]) if packet else 0x0
        self.client_ip_address = BytesToData.bytesToIp(packet[12:16]) if packet else '0.0.0.0'
        self.your_ip_address =  BytesToData.bytesToIp(packet[16:20]) if packet else '0.0.0.0'
        self.server_ip_address = BytesToData.bytesToIp(packet[20:24]) if packet else '0.0.0.0'
        self.gateway_ip_address = BytesToData.bytesToIp(packet[24:28]) if packet else '0.0.0.0'
        self.client_hardware_address =  BytesToData.bytesToMac(packet[28:34]) if packet else '1A:2B:3C:3C:C4:EF'
        self.server_name = BytesToData.bytesToStr(packet[44:108]) if packet else ''
        self.boot_filename = BytesToData.bytesToStr(packet[108:236]) if packet else ''
        self.magic_cookie = BytesToData.bytesToStr(packet[236:240]) if packet else int.from_bytes(b'\x63\x82\x53\x63', byteorder='big') #standard value: 99.130.83.99

    def pregateste_packetul(self):
        packet_pregatit = b''
        packet_pregatit += DataToBytes.intToBytes(self.opcode)
        packet_pregatit += DataToBytes.intToBytes(self.hardware_type)
        packet_pregatit += DataToBytes.intToBytes(self.hardware_address_length)
        packet_pregatit += DataToBytes.intToBytes(self.hops)
        packet_pregatit += DataToBytes.hexToBytes(self.transaction_id)
        packet_pregatit += DataToBytes.intToBytes(self.seconds_elapsed)
        packet_pregatit += DataToBytes.hexToBytes(self.boot_flags, 2)
        packet_pregatit += DataToBytes.ipToBytes(self.client_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.your_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.server_ip_address)
        packet_pregatit += DataToBytes.ipToBytes(self.gateway_ip_address)
        packet_pregatit += DataToBytes.macToBytes(self.client_hardware_address)
        packet_pregatit += DataToBytes.strToBytes(self.server_name, 64)
        packet_pregatit += DataToBytes.strToBytes(self.boot_filename, 128)
        packet_pregatit += DataToBytes.hexToBytes(self.magic_cookie, 4)
        #OPTIUNI
        return packet_pregatit

    def __str__(self):
        msg: str = f"""
        opcode: {self.opcode}\n
        hardware_type: {self.hardware_type}\n
        hardware_address_length: {self.hardware_address_length}\n
        hops: {self.hops}\n
        transaction_id: {self.transaction_id}\n
        seconds_elapsed: {self.seconds_elapsed}\n
        boot_flags: {self.boot_flags}\n
        client_ip_address: {self.client_ip_address}\n
        your_ip_address: {self.your_ip_address}\n
        server_ip_address: {self.server_ip_address}\n
        gateway_ip_address: {self.gateway_ip_address}\n
        client_hardware_address: {self.client_hardware_address}\n
        server_name: {self.server_name}\n
        boot_filename: {self.boot_filename}\n
        """
        return msg

# OPTIUNI, DESPACHETARE

