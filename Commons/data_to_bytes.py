import socket


class DataToBytes:
    @staticmethod
    def ip_to_bytes(data: str) -> bytes:
        """
        Transforms an ip dotted form to bytes form
        :param data: The ip address in dotted form
        :return: Ip address in byte form
        """
        return socket.inet_aton(data)

    @staticmethod
    def hex_to_bytes(data, length: int = 4) -> bytes:
        """
        Transforms hexadecimal values to bytes
        :param data: hexadecimal value to be transformed
        :param length: length of the returned bytes
        :return: Hexadecimal values in byte form
        """
        return data.to_bytes(length, 'big')

    @staticmethod
    def int_to_bytes(data: int, length: int = 1) -> bytes:
        """
        Transforms integer values to bytes
        :param data: integer value to be transformed
        :param length: length of the returned bytes
        :return: integer values parsed to bytes
        """
        return data.to_bytes(length, 'big')

    @staticmethod
    def mac_to_bytes(address: str, length: int = 6) -> bytes:
        """
        Transforms a MAC address with colons form to bytes
        :param address: MAC address with colons form
        :param length: length of the returned bytes
        :return: MAC address in byte form
        """
        address_list = list(map(lambda byte: bytes.fromhex(byte), address.split(":")))
        padding = b'\x00' * (length - len(address_list))
        final = b''.join(address_list) + padding
        return final + (length - len(final)) * b'\x00'

    @staticmethod
    def str_to_bytes(data: str, length: int) -> bytes:
        """
        Transforms string values to bytes
        :param data: string to be parsed
        :param length: length of the returned bytes
        :return: input string in byte form
        """
        final = str.encode(data)
        padding = (length - len(final)) * b'\x00'
        return final + padding
