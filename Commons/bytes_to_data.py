class BytesToData:
    @staticmethod
    def bytes_to_ip(data: bytes) -> str:
        """Transforms an ip address from bytes to decimal dotted form

        :param data: Ip address in bytes
        :return: Ip address in decimal dotted form
        """
        arr = [int(x) for x in data]
        ip = '.'.join(str(x) for x in arr)
        return str(ip)

    @staticmethod
    def bytes_to_hex(data: bytes) -> int:
        """Transforms bytes into hexadecimal numbers

        :param data: bytes to be parsed
        :return: hexadecimal value
        """
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        """Transforms bytes into string

        :param data: bytes to be transformed
        :return: input bytes parsed to string
        """
        final = data.decode("utf-8")
        return final.replace('\0', '')

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        """Transforms byte into integer

        :param data: bytes to be transformed
        :return: input bytes parsed to int
        """
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytes_to_mac(data: bytes) -> str:
        """Tranforms a MAC address from bytes to hexadecimal with colons format

        :param data: bytes to be transformed
        :return: input bytes parsed to hexadecimal with colons format
        """
        rez = ''
        for x in data:
            hexadecimal_value = str(hex(x)[2:])
            padding = (2 - len(hexadecimal_value)) * '0'
            rez += padding + hexadecimal_value + ":"
        return rez[:-1]
