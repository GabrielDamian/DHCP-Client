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
        final = bytes.fromhex(data.replace(':', '').lower())
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

    #TO DO: MAC

class Opcodes(IntEnum):
    NONE = 0
    REQUEST = 1
    REPLY = 2


class Packet:
    def __init__(self,packet):
        self.opcode = Opcodes(BytesToData.int(packet[0:1])) if packet else Opcodes.NONE
        self.hardware_type = BytesToData.int(packet[1:2]) if packet else 1  #1 - Ethernet
        self.hardware_address_length = BytesToData.int(packet[2:3]) if packet else 6
        self.hops = BytesToData.int(packet[3:4]) if packet else 0 #noduri intermediare prin care a trecut mesajul
        self.transaction_id = BytesToData.hex(packet[4:8]) if packet else randrange(0x1_00_00_00_00) #token random de identificare mesaj propriu
        self.seconds_elapsed = BytesToData.int(packet[8:10]) if packet else 0 #number of seconds elapsed since a client began an attempt to acquire or renew a lease
        self.boot_flags = BytesToData.hex(packet[10:12]) if packet else 0x0
        self.client_ip_address = BytesToData.ip(packet[12:16]) if packet else '0.0.0.0'
        self.your_ip_address =  BytesToData.ip(packet[16:20]) if packet else '0.0.0.0'
        self.server_ip_address = BytesToData.ip(packet[20:24]) if packet else '0.0.0.0'
        self.gateway_ip_address = BytesToData.ip(packet[24:28]) if packet else '0.0.0.0'
        self.client_hardware_address =  BytesToData.mac(packet[28:34]) if packet else '1A:2B:3C:3C:C4:EF'
        self.server_name = BytesToData.str(packet[44:108]) if packet else ''
        self.boot_filename =  BytesToData.str(packet[108:236]) if packet else ''
        self.magic_cookie = BytesToData.int(packet[236:240]) if packet else int.from_bytes(b'\x63\x82\x53\x63', byteorder='big') #standard value: 99.130.83.99


