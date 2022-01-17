import socket


class DataToBytes:
    @staticmethod
    def ip_to_bytes(data: str) -> bytes:
        return socket.inet_aton(data)

    @staticmethod
    def hex_to_bytes(data, length: int = 4) -> bytes:
        return data.to_bytes(length, 'big')

    @staticmethod
    def int_to_bytes(data: int, length: int = 1) -> bytes:
        return data.to_bytes(length, 'big')

    @staticmethod
    def mac_to_bytes(address: str, length: int = 6) -> bytes:
        address_list = list(map(lambda byte: bytes.fromhex(byte), address.split(":")))
        padding = b'\x00' * (length - len(address_list))
        final = b''.join(address_list) + padding
        return final + (length - len(final)) * b'\x00'

    @staticmethod
    def str_to_bytes(data: str, length: int) -> bytes:
        final = str.encode(data)
        padding = (length - len(final)) * b'\x00'
        return final + padding
