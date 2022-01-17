class BytesToData:
    @staticmethod
    def bytes_to_ip(data: bytes) -> str:
        arr = [int(x) for x in data]
        ip = '.'.join(str(x) for x in arr)
        return str(ip)

    @staticmethod
    def bytes_to_hex(data: bytes) -> int:
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        final = data.decode("utf-8")
        return final.replace('\0', '')

    @staticmethod
    def bytes_to_int(data: bytes) -> int:
        return int.from_bytes(data, byteorder='big', signed=False)

    @staticmethod
    def bytes_to_mac(data: bytes) -> str:
        rez = ''
        for x in data:
            hexazecimal_value = str(hex(x)[2:])
            padding = (2 - len(hexazecimal_value)) * '0'
            rez += padding + hexazecimal_value + ":"
        return rez[:-1]
