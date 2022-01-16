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
    def mac_to_bytes(data: str, length: int = 6) -> bytes:
        vec = [bytes.fromhex(x).lower() for x in data.split(":")]
        final = b''
        for e in vec:
            final += e
        return final + (length - final.__len__()) * b'\x00'

    @staticmethod
    def str_to_bytes(data: str, length: int) -> bytes:
        final = str.encode(data)
        return final + (length - len(final)) * b'\x00'